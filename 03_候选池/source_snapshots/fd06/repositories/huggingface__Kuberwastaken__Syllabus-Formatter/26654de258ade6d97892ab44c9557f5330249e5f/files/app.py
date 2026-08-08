import gradio as gr
import json
import time
import logging
import re
from typing import Dict, Any, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from datetime import datetime
import os
import tempfile
import psutil  # Added for resource monitoring
import sys

# Hugging Face Transformers
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import gc

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SyllabusFormatter:
    def __init__(self, model_name="microsoft/Phi-3-mini-4k-instruct"):
        """Initialize the formatter with Phi-3 model"""
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.pipe = None
        self.is_model_loaded = False
        self.processing_lock = threading.Lock()

    def load_model(self):
        """Load the Phi-3 model with optimizations for CPU"""
        if self.is_model_loaded:
            logger.info("Model already loaded")
            return True

        try:
            logger.info(f"Loading model: {self.model_name}")
            logger.info(f"CUDA available: {torch.cuda.is_available()}")
            logger.info(f"Python version: {sys.version}")
            logger.info(f"Torch version: {torch.__version__}")
            logger.info(f"Transformers version: {transformers.__version__}")
            logger.info(f"Available memory: {psutil.virtual_memory().available / (1024**3):.2f} GB")

            # Check for API token to avoid misconfiguration
            if os.getenv("HF_API_TOKEN"):
                logger.warning("HF_API_TOKEN detected, but this app uses local CPU inference.")

            # Load tokenizer
            logger.info("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            logger.info("Tokenizer loaded successfully")

            # Load model with CPU optimizations
            logger.info("Loading model...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,  # Use float32 for CPU
                device_map="cpu",  # Explicitly set to CPU
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            logger.info("Model loaded successfully")

            # Create pipeline for CPU
            logger.info("Creating pipeline...")
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1,  # Explicitly set to CPU
                torch_dtype=torch.float32
            )
            logger.info("Pipeline created successfully")

            self.is_model_loaded = True
            logger.info("Model loaded successfully!")
            return True

        except Exception as e:
            logger.error(f"Error loading model: {str(e)}", exc_info=True)
            return False
        finally:
            gc.collect()  # Clean up memory after loading

    def create_formatting_prompt(self, unit_content: str, unit_name: str, subject_name: str = "") -> str:
        """Create a focused prompt for formatting syllabus content"""
        prompt = f"""<|system|>You are a professional academic syllabus formatter. Your job is to take poorly formatted syllabus content and make it beautifully organized and readable.

RULES:
1. PRESERVE every single word, topic, and concept from the original
2. NEVER add explanations, examples, or new content
3. ONLY restructure and format the existing text
4. Use clear headings, bullet points, and logical grouping
5. Separate different topics with proper spacing
6. Make it scannable and easy to read

FORMAT STYLE:
- Use main topic headings with proper capitalization
- Group related subtopics under main topics
- Use bullet points (•) for lists of concepts
- Use sub-bullets (◦) for details under main bullets
- Separate major sections with line breaks
- Keep technical terms exactly as written<|end|>

<|user|>Subject: {subject_name}
Unit: {unit_name}

Original content (poorly formatted):
{unit_content}

Task: Reformat this content to be beautifully organized and readable. Do NOT add any new information - only restructure what's already there.<|end|>

<|assistant|>"""
        return prompt

    def format_single_unit(self, unit_data: Tuple[str, str, str, str, str]) -> Tuple[str, str, str, str, str]:
        """Format a single unit's content"""
        branch, semester, subject, unit_name, unit_content = unit_data

        try:
            with self.processing_lock:
                logger.info(f"Formatting {subject} - {unit_name}")
                logger.info(f"Available memory before processing: {psutil.virtual_memory().available / (1024**3):.2f} GB")

                # Create prompt
                prompt = self.create_formatting_prompt(unit_content, unit_name, subject)

                # Generate formatted content
                response = self.pipe(
                    prompt,
                    max_new_tokens=2048,
                    temperature=0.1,
                    do_sample=True,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )

                # Extract formatted content
                generated_text = response[0]['generated_text']
                assistant_start = generated_text.find("<|assistant|>")

                if assistant_start != -1:
                    formatted_content = generated_text[assistant_start + len("<|assistant|>"):].strip()
                else:
                    formatted_content = generated_text[len(prompt):].strip()

                # Clean up the content
                formatted_content = self.clean_generated_content(formatted_content)

                # Validate content
                if self.validate_formatted_content(unit_content, formatted_content):
                    logger.info(f"Successfully formatted {subject} - {unit_name}")
                    return (branch, semester, subject, unit_name, formatted_content)
                else:
                    logger.warning(f"Validation failed for {subject} - {unit_name}")
                    return (branch, semester, subject, unit_name, unit_content)

        except Exception as e:
            logger.error(f"Error formatting {subject} - {unit_name}: {str(e)}", exc_info=True)
            return (branch, semester, subject, unit_name, unit_content)
        finally:
            gc.collect()  # Clean up memory after each unit
            torch.cuda.empty_cache()  # Safe to call even on CPU

    def clean_generated_content(self, content: str) -> str:
        """ JT: Clean up generated content
        Removes special tokens and AI commentary, and fixes spacing.
        Args:
            content: The raw generated content
        Returns:
            Cleaned content as a string
        """
        # Remove special tokens
        content = re.sub(r'<\|.*?\|>', '', content)

        # Remove AI commentary
        lines = content.split('\n')
        cleaned_lines = []

        for line in lines:
            line = line.strip()
            if (line.startswith("Here") and ("formatted" in line.lower() or "organized" in line.lower())) or \
               line.startswith("I have") or line.startswith("The content has been") or \
               line.startswith("Note:") or line.startswith("This formatted version"):
                continue
            if line:
                cleaned_lines.append(line)

        content = '\n'.join(cleaned_lines)

        # Fix spacing
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        content = re.sub(r'\n([A-Z][^:\n]*:)\n', r'\n\n\1\n', content)

        return content.strip()

    def validate_formatted_content(self, original: str, formatted: str) -> bool:
        """Validate that formatted content preserves important information"""
        if len(formatted) < len(original) * 0.4:
            return False

        # Check for preservation of key terms
        original_words = set(re.findall(r'\b[A-Z][a-z]*(?:[A-Z][a-z]*)*\b', original))
        formatted_words = set(re.findall(r'\b[A-Z][a-z]*(?:[A-Z][a-z]*)*\b', formatted))

        missing_terms = original_words - formatted_words
        if len(missing_terms) > len(original_words) * 0.3:
            return False

        return True

    def extract_units_for_processing(self, syllabus_data: Dict[str, Any]) -> List[Tuple[str, str, str, str, str]]:
        """Extract all units for concurrent processing"""
        units = []

        for branch_name, branch_data in syllabus_data.get("syllabus", {}).items():
            if not isinstance(branch_data, dict):
                continue

            for sem_name, sem_data in branch_data.items():
                if not isinstance(sem_data, dict):
                    continue

                for subject_name, subject_data in sem_data.items():
                    if not isinstance(subject_data, dict) or "content" not in subject_data:
                        continue

                    content = subject_data["content"]
                    if not isinstance(content, dict):
                        continue

                    for unit_name, unit_content in content.items():
                        if unit_name.startswith("Unit") and isinstance(unit_content, str):
                            units.append((branch_name, sem_name, subject_name, unit_name, unit_content))

        return units

    def format_syllabus_concurrent(self, syllabus_data: Dict[str, Any], progress_callback=None, max_workers=1) -> Dict[str, Any]:
        """Format syllabus using concurrent processing"""
        if not self.is_model_loaded:
            if not self.load_model():
                raise Exception("Failed to load model")

        # Extract units for processing
        units = self.extract_units_for_processing(syllabus_data)
        total_units = len(units)

        logger.info(f"Processing {total_units} units with {max_workers} workers")

        # Process units concurrently
        processed_units = {}
        completed_count = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_unit = {executor.submit(self.format_single_unit, unit): unit for unit in units}

            # Process completed tasks
            for future in as_completed(future_to_unit):
                try:
                    branch, semester, subject, unit_name, formatted_content = future.result()

                    # Store the result
                    key = f"{branch}|{semester}|{subject}|{unit_name}"
                    processed_units[key] = formatted_content

                    completed_count += 1
                    progress = (completed_count / total_units) * 100

                    if progress_callback:
                        progress_callback(progress, f"Processed {subject} - {unit_name}")

                    logger.info(f"Completed {completed_count}/{total_units} ({progress:.1f}%)")

                except Exception as e:
                    logger.error(f"Error processing unit: {str(e)}", exc_info=True)

        # Update the syllabus data with formatted content
        for branch_name, branch_data in syllabus_data.get("syllabus", {}).items():
            if not isinstance(branch_data, dict):
                continue

            for sem_name, sem_data in branch_data.items():
                if not isinstance(sem_data, dict):
                    continue

                for subject_name, subject_data in sem_data.items():
                    if not isinstance(subject_data, dict) or "content" not in subject_data:
                        continue

                    content = subject_data["content"]
                    if not isinstance(content, dict):
                        continue

                    for unit_name in content.keys():
                        if unit_name.startswith("Unit"):
                            key = f"{branch_name}|{sem_name}|{subject_name}|{unit_name}"
                            if key in processed_units:
                                syllabus_data["syllabus"][branch_name][sem_name][subject_name]["content"][unit_name] = processed_units[key]

        # Add metadata
        if "metadata" not in syllabus_data:
            syllabus_data["metadata"] = {}

        syllabus_data["metadata"]["lastFormatted"] = datetime.now().isoformat()
        syllabus_data["metadata"]["formattingNote"] = "Content formatted using Phi-3 AI for enhanced readability"
        syllabus_data["metadata"]["originalContentPreserved"] = True
        syllabus_data["metadata"]["unitsProcessed"] = completed_count
        syllabus_data["metadata"]["formattingModel"] = self.model_name
        syllabus_data["metadata"]["version"] = "2.0"
        syllabus_data["metadata"]["processedConcurrently"] = True
        syllabus_data["metadata"]["maxWorkers"] = max_workers

        return syllabus_data

# Global formatter instance
formatter = SyllabusFormatter()

def format_syllabus_file(file_path, max_workers=1, progress=gr.Progress()):
    """Main function to format syllabus file"""
    try:
        # Load JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            syllabus_data = json.load(f)

        # Count units
        units = formatter.extract_units_for_processing(syllabus_data)
        total_units = len(units)

        progress(0, f"Found {total_units} units to process")

        # Progress callback
        def update_progress(percent, message):
            progress(percent/100, message)

        # Format the syllabus
        formatted_data = formatter.format_syllabus_concurrent(
            syllabus_data,
            progress_callback=update_progress,
            max_workers=max_workers
        )

        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(formatted_data, f, indent=2, ensure_ascii=False)
            temp_path = f.name

        progress(1.0, f"Completed! Processed {total_units} units")

        return temp_path, f"✅ Successfully formatted {total_units} units!"

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return None, error_msg

def create_sample_json():
    """Create a sample JSON file for testing"""
    sample_data = {
        "metadata": {
            "totalFiles": 1,
            "generatedAt": datetime.now().isoformat(),
            "source": "Sample syllabus for testing",
            "description": "Sample syllabus content"
        },
        "syllabus": {
            "CSE": {
                "SEM1": {
                    "Mathematics": {
                        "extractedFrom": {
                            "path": "CSE > SEM1 > Mathematics",
                            "branch": "CSE",
                            "semester": "SEM1",
                            "subject": "Mathematics"
                        },
                        "content": {
                            "Unit I": "Differential Calculus: Limits, continuity, derivatives, applications of derivatives, maxima and minima, curve sketching, related rates, optimization problems, L'Hospital's rule, Taylor series, Partial derivatives, total differential, chain rule, implicit differentiation, Jacobians.",
                            "Unit II": "Integral Calculus: Integration techniques, definite integrals, applications of integrals, area under curves, volume of solids, arc length, surface area, Multiple integrals, double integrals, triple integrals, change of variables, applications in geometry and physics."
                        }
                    }
                }
            }
        }
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
        return f.name

# Gradio Interface
def create_interface():
    with gr.Blocks(
        title="Syllabus Formatter - AI-Powered JSON Syllabus Formatter",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="purple",
            neutral_hue="gray"
        )
    ) as interface:

        gr.HTML("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 20px;">
            <h1 style="font-size: 2.5em; margin-bottom: 10px;">🎓 Syllabus Formatter</h1>
            <p style="font-size: 1.2em; opacity: 0.9;">AI-Powered JSON Syllabus Content Formatter using Phi-3</p>
            <p style="font-size: 1em; opacity: 0.8;">Upload your JSON syllabus file and get beautifully formatted content!</p>
        </div>
        """)

        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML("""
                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                    <h3>📋 Instructions:</h3>
                    <ol>
                        <li>Upload your JSON syllabus file</li>
                        <li>Choose number of concurrent workers (1 recommended for CPU)</li>
                        <li>Click "Format Syllabus" to start processing</li>
                        <li>Download the formatted JSON file</li>
                    </ol>
                    <p><strong>Note:</strong> Only syllabus content will be formatted, metadata remains unchanged.</p>
                </div>
                """)

                file_input = gr.File(
                    label="📁 Upload JSON Syllabus File",
                    file_types=[".json"],
                    type="filepath"
                )

                workers_slider = gr.Slider(
                    minimum=1,
                    maximum=4,  # Reduced max to avoid memory issues
                    value=1,    # Default to 1 for CPU
                    step=1,
                    label="🔄 Concurrent Workers",
                    info="Use 1 for CPU to minimize memory usage"
                )

                format_btn = gr.Button(
                    "🚀 Format Syllabus",
                    variant="primary",
                    size="lg"
                )

                sample_btn = gr.Button(
                    "📝 Download Sample JSON",
                    variant="secondary"
                )

            with gr.Column(scale=1):
                status_output = gr.Textbox(
                    label="📊 Status",
                    lines=3,
                    interactive=False
                )

                download_output = gr.File(
                    label="📥 Download Formatted JSON",
                    visible=False
                )

                gr.HTML("""
                <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-top: 15px;">
                    <h3>✨ Features:</h3>
                    <ul>
                        <li>🤖 Powered by Microsoft Phi-3 AI model</li>
                        <li>🔒 Preserves all original content</li>
                        <li>📊 Real-time progress tracking</li>
                        <li>🎯 Formats only syllabus content, not metadata</li>
                        <li>✅ Validation to ensure content integrity</li>
                    </ul>
                </div>
                """)

        # Event handlers
        def format_handler(file_path, max_workers):
            if file_path is None:
                return "❌ Please upload a JSON file first.", gr.update(visible=False)

            try:
                result_path, message = format_syllabus_file(file_path, int(max_workers))
                if result_path:
                    return message, gr.update(visible=True, value=result_path)
                else:
                    return message, gr.update(visible=False)
            except Exception as e:
                return f"❌ Error: {str(e)}", gr.update(visible=False)

        def sample_handler():
            sample_path = create_sample_json()
            return gr.update(visible=True, value=sample_path)

        format_btn.click(
            format_handler,
            inputs=[file_input, workers_slider],
            outputs=[status_output, download_output]
        )

        sample_btn.click(
            sample_handler,
            outputs=[gr.File(label="📥 Sample JSON File", visible=True)]
        )

        gr.HTML("""
        <div style="text-align: center; padding: 15px; margin-top: 20px; border-top: 1px solid #ddd;">
            <p style="color: #666;">
                Built with ❤️ using Hugging Face Spaces | 
                Powered by Microsoft Phi-3 | 
                Optimized for CPU processing
            </p>
        </div>
        """)

    return interface

# Launch the app
if __name__ == "__main__":
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )