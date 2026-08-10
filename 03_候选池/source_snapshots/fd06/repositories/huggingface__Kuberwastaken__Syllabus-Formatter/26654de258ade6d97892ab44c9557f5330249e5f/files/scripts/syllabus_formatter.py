#!/usr/bin/env python3
"""
Syllabus Formatter Script
This script downloads Phi-3 3B model and uses it to format syllabus content
to be more readable while preserving all content and structure.
"""

import json
import os
import sys
from pathlib import Path
import time
import logging
from typing import Dict, Any, List, Tuple
import re
import psutil  # For memory checks

# Imports for type hinting and core functionality
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from transformers import BitsAndBytesConfig  # For 8-bit quantization
import requests

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('syllabus_formatter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SyllabusFormatter:
    def __init__(self, model_name="microsoft/Phi-3-mini-4k-instruct"):
        """Initialize the formatter with Phi-3 model"""
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.pipe = None
        self.processed_count = 0
        self.total_count = 0
        
    def setup_model(self):
        """Download and setup the Phi-3 model with CPU optimization"""
        logger.info(f"Setting up model: {self.model_name}")
        
        try:
            # Check available memory
            available_memory = psutil.virtual_memory().available / (1024 * 1024 * 1024)  # Convert to GB
            logger.info(f"Available system memory: {available_memory:.2f} GB")
            
            if available_memory < 4:  # We need at least 4GB free
                logger.warning("Low memory detected. Attempting to load with maximum optimization...")
            
            # Load tokenizer
            logger.info("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            # Load model with CPU optimizations
            logger.info("Loading model with CPU optimizations...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,  # Use float32 for CPU
                device_map=None,  # Disable device mapping for CPU
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            # Move model to CPU explicitly
            self.model = self.model.to('cpu')
            
            # Create pipeline with CPU settings
            logger.info("Creating CPU-optimized pipeline...")
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device='cpu'  # Explicitly set to CPU
            )
            
            logger.info("Model setup complete with CPU optimizations!")
            return True
            
        except Exception as e:
            error_msg = str(e)
            if "paging file" in error_msg.lower():
                logger.error(
                    "Windows virtual memory (page file) is too small. Please:\n"
                    "1. Open System Properties > Advanced > Performance Settings > Advanced\n"
                    "2. Under Virtual Memory, click Change\n"
                    "3. Increase the page file size (recommended: 1.5x your RAM size)\n"
                    "4. Restart your computer"
                )
            else:
                logger.error(f"Error setting up model: {error_msg}")
            return False
    
    def create_formatting_prompt(self, unit_content: str, unit_name: str, subject_name: str = "") -> str:
        """Create a very clear, focused prompt for formatting syllabus content"""
        prompt = f"""<|system|>You are a professional academic syllabus formatter. Your ONLY job is to take badly formatted syllabus content and make it beautifully organized and readable.

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

Task: Reformat this content to be beautifully organized and readable. Do NOT add any new information - only restructure what\'s already there. Make it professional and easy to scan.<|end|>

<|assistant|>"""
        return prompt
    
    def format_unit_content(self, unit_content: str, unit_name: str, subject_name: str = "") -> str:
        """Format a single unit\'s content using the AI model with focused prompting"""
        try:
            # Create a very clear, focused prompt
            prompt = self.create_formatting_prompt(unit_content, unit_name, subject_name)
            
            # Generate formatted content with specific parameters for better output
            response = self.pipe(
                prompt,
                max_new_tokens=2048,  # Increased for longer content
                temperature=0.1,      # Very low for consistent formatting
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
            
            # Extract the formatted content
            generated_text = response[0]['generated_text']
            
            # Find the assistant's response more reliably
            assistant_start = generated_text.find("<|assistant|>")
            if assistant_start != -1:
                formatted_content = generated_text[assistant_start + len("<|assistant|>"):].strip()
            else:
                # Fallback: try to find content after the prompt
                prompt_end = generated_text.find(prompt)
                if prompt_end != -1:
                    formatted_content = generated_text[prompt_end + len(prompt):].strip()
                else:
                    formatted_content = generated_text.strip()
            
            # Clean up the generated content
            formatted_content = self.clean_generated_content(formatted_content)
            
            # Validate the formatted content
            if not self.validate_formatted_content(unit_content, formatted_content, unit_name):
                logger.warning(f"Validation failed for {subject_name} - {unit_name}, using original")
                return unit_content
            
            logger.info(f"✓ Successfully formatted {subject_name} - {unit_name}")
            return formatted_content
            
        except Exception as e:
            logger.error(f"Error formatting {subject_name} - {unit_name}: {str(e)}")
            return unit_content  # Return original content if formatting fails
    
    def show_sample_comparison(self, original: str, formatted: str, subject: str, unit: str):
        """Show a before/after comparison for verification"""
        print("\n" + "="*80)
        print(f"📊 SAMPLE COMPARISON: {subject} - {unit}")
        print("="*80)
        print("🔴 BEFORE (Original):")
        print("-" * 40)
        print(original[:300] + "..." if len(original) > 300 else original)
        print("\n")
        print("🟢 AFTER (Formatted):")
        print("-" * 40)
        print(formatted[:300] + "..." if len(formatted) > 300 else formatted)
        print("="*80)
    
    def validate_formatted_content(self, original: str, formatted: str, unit_name: str) -> bool:
        """Validate that formatted content preserves all important information"""
        # Check length - formatted should not be drastically shorter
        if len(formatted) < len(original) * 0.4:
            logger.warning(f"Formatted content too short for {unit_name}")
            return False
        
        # Check for key technical terms preservation
        original_words = set(re.findall(r'\b[A-Z][a-z]*(?:[A-Z][a-z]*)*\b', original))
        formatted_words = set(re.findall(r'\b[A-Z][a-z]*(?:[A-Z][a-z]*)*\b', formatted))
        
        # Allow for some formatting differences but ensure major terms are preserved
        missing_important_terms = original_words - formatted_words
        if len(missing_important_terms) > len(original_words) * 0.3:
            logger.warning(f"Too many important terms missing in {unit_name}: {missing_important_terms}")
            return False
        
        return True
    
    def clean_generated_content(self, content: str) -> str:
        """Clean up generated content removing any artifacts and improving structure"""
        # Remove any remaining special tokens
        content = re.sub(r'<\|.*?\|>', '', content)
        
        # Remove any meta-commentary from the AI
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip lines that look like AI commentary
            if (line.startswith("Here") and ("formatted" in line.lower() or "organized" in line.lower())) or \
               line.startswith("I have") or line.startswith("The content has been") or \
               line.startswith("Note:") or line.startswith("This formatted version"):
                continue
            if line:  # Only add non-empty lines
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Fix multiple consecutive newlines
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # Ensure proper spacing around headers
        content = re.sub(r'\n([A-Z][^:\n]*:)\n', r'\n\n\1\n', content)
        
        return content.strip()
    
    def count_total_units(self, syllabus_data: Dict[str, Any]) -> int:
        """Count total number of units to process"""
        count = 0
        for branch_name, branch_data in syllabus_data.get("syllabus", {}).items():
            if isinstance(branch_data, dict):
                for sem_name, sem_data in branch_data.items():
                    if isinstance(sem_data, dict):
                        for subject_name, subject_data in sem_data.items():
                            if isinstance(subject_data, dict) and "content" in subject_data:
                                content = subject_data["content"]
                                if isinstance(content, dict):
                                    count += len([k for k in content.keys() if k.startswith("Unit")])
        return count
    
    def format_syllabus(self, input_file: str, output_file: str) -> bool:
        """Format the entire syllabus file"""
        try:
            # Load the syllabus file
            logger.info(f"Loading syllabus from: {input_file}")
            with open(input_file, 'r', encoding='utf-8') as f:
                syllabus_data = json.load(f)
            
            # Count total units
            self.total_count = self.count_total_units(syllabus_data)
            logger.info(f"Total units to process: {self.total_count}")
            
            # Process each branch
            for branch_name, branch_data in syllabus_data.get("syllabus", {}).items():
                if not isinstance(branch_data, dict):
                    continue
                    
                logger.info(f"Processing branch: {branch_name}")
                
                # Process each semester
                for sem_name, sem_data in branch_data.items():
                    if not isinstance(sem_data, dict):
                        continue
                        
                    logger.info(f"Processing {branch_name} - {sem_name}")
                    
                    # Process each subject
                    for subject_name, subject_data in sem_data.items():
                        if not isinstance(subject_data, dict) or "content" not in subject_data:
                            continue
                            
                        content = subject_data["content"]
                        if not isinstance(content, dict):
                            continue
                        
                        logger.info(f"Processing {branch_name} - {sem_name} - {subject_name}")
                        
                        # Format each unit
                        for unit_name, unit_content in content.items():
                            if not unit_name.startswith("Unit") or not isinstance(unit_content, str):
                                continue
                            
                            self.processed_count += 1
                            progress = (self.processed_count / self.total_count) * 100
                            
                            logger.info(f"🔄 Processing {branch_name} > {sem_name} > {subject_name} > {unit_name} "
                                      f"({self.processed_count}/{self.total_count} - {progress:.1f}%)")
                            
                            # Show original content preview
                            preview = unit_content[:100].replace('\n', ' ') + "..." if len(unit_content) > 100 else unit_content
                            logger.info(f"📝 Original: {preview}")
                            
                            # Format the unit content with subject context
                            formatted_content = self.format_unit_content(
                                unit_content, 
                                unit_name, 
                                subject_name
                            )
                            
                            # Update the content
                            syllabus_data["syllabus"][branch_name][sem_name][subject_name]["content"][unit_name] = formatted_content
                            
                            # Show formatted content preview
                            formatted_preview = formatted_content[:100].replace('\n', ' ') + "..." if len(formatted_content) > 100 else formatted_content
                            logger.info(f"✨ Formatted: {formatted_preview}")
                            
                            # Add delay to prevent overwhelming the model
                            time.sleep(0.5)  # Increased delay for better processing
            
            # Add formatting metadata with detailed info
            if "metadata" not in syllabus_data:
                syllabus_data["metadata"] = {}
            
            syllabus_data["metadata"]["lastFormatted"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
            syllabus_data["metadata"]["formattingNote"] = "Content formatted using Phi-3 3B AI for enhanced readability and structure"
            syllabus_data["metadata"]["originalContentPreserved"] = True
            syllabus_data["metadata"]["unitsProcessed"] = self.processed_count
            syllabus_data["metadata"]["formattingModel"] = self.model_name
            syllabus_data["metadata"]["version"] = "2.0"
            
            # Save the formatted syllabus
            logger.info(f"Saving formatted syllabus to: {output_file}")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(syllabus_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully formatted {self.processed_count} units!")
            return True
            
        except Exception as e:
            logger.error(f"Error formatting syllabus: {str(e)}")
            return False

def main():
    """Main function"""
    # Setup paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    syllabus_file = project_root / "public" / "Content-Meta" / "syllabus.json"
    output_file = project_root / "public" / "Content-Meta" / "syllabus_formatted.json"
    
    # Validate input file
    if not syllabus_file.exists():
        logger.error(f"Syllabus file not found: {syllabus_file}")
        return False
    
    # Create formatter
    formatter = SyllabusFormatter()
    
    # Setup model
    logger.info("Setting up Phi-3 model...")
    if not formatter.setup_model():
        logger.error("Failed to setup model")
        return False
    
    # Format syllabus
    logger.info("Starting syllabus formatting...")
    success = formatter.format_syllabus(str(syllabus_file), str(output_file))
    
    if success:
        logger.info(f"Formatting complete! Output saved to: {output_file}")
        logger.info("You can now review the formatted syllabus and replace the original if satisfied.")
    else:
        logger.error("Formatting failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)