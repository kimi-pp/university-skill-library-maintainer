import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from datetime import datetime
import gradio as gr
from typing import Dict, List, Union, Optional
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentAnalyzer:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self.categories = [
            "Violence", "Death", "Substance Use", "Gore", 
            "Vomit", "Sexual Content", "Sexual Abuse", 
            "Self-Harm", "Gun Use", "Animal Cruelty", 
            "Mental Health Issues"
        ]
        self.pattern = re.compile(r'\b(' + '|'.join(self.categories) + r')\b', re.IGNORECASE)
        logger.info(f"Initialized analyzer with device: {self.device}")
        self._load_model()

    def _load_model(self) -> None:
        """Load model and tokenizer with CPU optimization"""
        try:
            logger.info("Loading model components...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
                use_fast=True,
                truncation_side="left"
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            ).to(self.device).eval()
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Model loading failed: {str(e)}")
            raise

    def _chunk_text(self, text: str, max_tokens: int = 512) -> List[str]:
        """Context-aware chunking with token counting"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para_tokens = self.tokenizer.encode(para, add_special_tokens=False)
            para_length = len(para_tokens)
            
            if current_length + para_length > max_tokens and current_chunk:
                chunk_text = "\n\n".join(current_chunk)
                chunks.append(chunk_text)
                current_chunk = [para]
                current_length = para_length
            else:
                current_chunk.append(para)
                current_length += para_length
        
        if current_chunk:
            chunk_text = "\n\n".join(current_chunk)
            chunks.append(chunk_text)
            
        logger.info(f"Split text into {len(chunks)} chunks (max_tokens={max_tokens})")
        return chunks

    async def _analyze_chunk(self, chunk: str) -> tuple[List[str], str]:
        """Deep analysis with step-by-step reasoning"""
        prompt = f"""As a deep-thinking content analyzer, carefully evaluate this text for sensitive content.
Input text: {chunk}

Think through each step:
1. What is happening in the text?
2. What potentially sensitive themes or elements are present?
3. For each category below, is there clear evidence?

Categories: {", ".join(self.categories)}

Detailed analysis:
"""

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True).to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    max_length=8192
                )
            
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract categories more reliably using multiple patterns
            categories_found = set()
            
            # Look for explicit category mentions
            category_matches = self.pattern.findall(full_response.lower())
            
            # Normalize and validate matches
            for match in category_matches:
                for category in self.categories:
                    if match.lower() == category.lower():
                        categories_found.add(category)
            
            # Convert to list and sort for consistency
            matched_categories = sorted(list(categories_found))
            
            # Clean up reasoning text
            reasoning = full_response.split("\n\nCategories found:")[0] if "\n\nCategories found:" in full_response else full_response
            reasoning = reasoning.strip()
            
            if not matched_categories and any(trigger_word in full_response.lower() for trigger_word in 
                ["concerning", "warning", "caution", "trigger", "sensitive"]):
                logger.warning(f"Potential triggers found but no categories matched in chunk")
            
            logger.info(f"Chunk analysis complete - Categories found: {matched_categories}")
            return matched_categories, reasoning
            
        except Exception as e:
            logger.error(f"Chunk analysis error: {str(e)}")
            return [], f"Analysis error: {str(e)}"

    async def analyze_script(self, script: str, progress: Optional[gr.Progress] = None) -> tuple[List[str], List[str]]:
        """Main analysis workflow with progress updates"""
        if not script.strip():
            return ["No content provided"], ["No analysis performed"]
            
        identified_triggers = set()
        reasoning_outputs = []
        chunks = self._chunk_text(script)
        
        if not chunks:
            return ["Empty text after chunking"], ["No analysis performed"]
            
        total_chunks = len(chunks)
        
        for idx, chunk in enumerate(chunks):
            if progress:
                progress((idx/total_chunks, f"Deep analysis of chunk {idx+1}/{total_chunks}"))
                
            chunk_triggers, chunk_reasoning = await self._analyze_chunk(chunk)
            identified_triggers.update(chunk_triggers)
            reasoning_outputs.append(f"Chunk {idx + 1} Analysis:\n{chunk_reasoning}")
            
            logger.info(f"Processed chunk {idx+1}/{total_chunks}, found triggers: {chunk_triggers}")
        
        if progress:
            progress((1.0, "Analysis complete"))
            
        final_triggers = sorted(list(identified_triggers)) if identified_triggers else ["None"]
        logger.info(f"Final triggers identified: {final_triggers}")
        return final_triggers, reasoning_outputs

async def analyze_content(
    script: str,
    progress: Optional[gr.Progress] = None
) -> Dict[str, Union[List[str], str]]:
    """Gradio interface function with enhanced trigger detection"""
    try:
        analyzer = ContentAnalyzer()
        triggers, reasoning_output = await analyzer.analyze_script(script, progress)
        
        # Extract triggers from detailed analysis
        detected_triggers = set()
        full_reasoning = "\n\n".join(reasoning_output)
        
        # Look for explicit category markers
        category_markers = [
            (r'\b(\w+):\s*\+', 1),  # Matches "Category: +"
            (r'\*\*(\w+(?:\s+\w+)?):\*\*[^\n]*?\bMarked with "\+"', 1),  # Matches "**Category:** ... Marked with "+"
            (r'(\w+(?:\s+\w+)?)\s*is clearly present', 1),  # Matches "Category is clearly present"
        ]
        
        for pattern, group in category_markers:
            matches = re.finditer(pattern, full_reasoning, re.IGNORECASE)
            for match in matches:
                category = match.group(group).strip()
                # Normalize category names to match predefined categories
                for predefined_category in analyzer.categories:
                    if category.lower() in predefined_category.lower():
                        detected_triggers.add(predefined_category)
        
        # Add any triggers found through direct pattern matching
        for category in analyzer.categories:
            pattern = fr'\b{re.escape(category)}\b.*?(present|evident|indicated|clear|obvious)'
            if re.search(pattern, full_reasoning, re.IGNORECASE):
                detected_triggers.add(category)
        
        # If no triggers were found through detailed analysis, fall back to original triggers
        final_triggers = sorted(list(detected_triggers)) if detected_triggers else triggers
        
        result = {
            "detected_triggers": final_triggers if final_triggers else ["None"],
            "confidence": "High confidence" if final_triggers and final_triggers != ["None"] else "No triggers found",
            "model": "DeepSeek-R1-Distill-Qwen-1.5B",
            "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analysis_reasoning": full_reasoning
        }
        
        logger.info(f"Enhanced analysis complete. Results: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return {
            "detected_triggers": ["Analysis error"],
            "confidence": "Error",
            "model": "DeepSeek-R1-Distill-Qwen-1.5B",
            "analysis_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analysis_reasoning": str(e),
            "error": str(e)
        }

if __name__ == "__main__":
    iface = gr.Interface(
        fn=analyze_content,
        inputs=gr.Textbox(lines=12, label="Paste Script Here", placeholder="Enter text to analyze..."),
        outputs=[
            gr.JSON(label="Analysis Results"),
            gr.Textbox(label="Analysis Reasoning", lines=10)
        ],
        title="TREAT - Trigger Analysis for Entertainment Texts",
        description="Deep analysis of scripts for sensitive content using AI",
        allow_flagging="never"
    )
    iface.launch(show_error=True)