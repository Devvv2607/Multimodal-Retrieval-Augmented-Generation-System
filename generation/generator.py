"""
Generator for producing answers using the local LLM.
"""

import logging
from typing import List, Dict, Any
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

logger = logging.getLogger(__name__)

class Generator:
    """Generator for LLM-based answer production."""
    
    def __init__(self, model_name: str = "microsoft/phi-3-mini-4k-instruct", 
                 max_tokens: int = 2048):
        """
        Initialize generator.
        
        Args:
            model_name: Name of the LLM to use
            max_tokens: Maximum tokens for generation
        """
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.model = None
        self.tokenizer = None
        self.device = None
        
        # Set environment variables for better GPU utilization
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
        
        self._load_model()
    
    def _load_model(self):
        """Load the LLM and tokenizer."""
        try:
            # Check if CUDA is available
            cuda_available = torch.cuda.is_available()
            logger.info(f"CUDA available: {cuda_available}")
            
            if cuda_available:
                # Get GPU info
                gpu_count = torch.cuda.device_count()
                gpu_name = torch.cuda.get_device_name(0) if gpu_count > 0 else "Unknown"
                logger.info(f"GPU Count: {gpu_count}, Primary GPU: {gpu_name}")
                
            self.device = "cuda" if cuda_available else "cpu"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Handle tokenizer padding token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Try to load model with accelerate if available
            try:
                # Use device_map="auto" for better GPU utilization
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    device_map="auto",
                    torch_dtype=torch.float16 if cuda_available else torch.float32,
                    trust_remote_code=True,
                    low_cpu_mem_usage=True
                )
                logger.info("Model loaded with device_map=auto")
            except Exception as e:
                logger.warning(f"Could not load model with device_map, trying without accelerate features: {str(e)}")
                # Fallback to loading without device_map
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    trust_remote_code=True,
                    low_cpu_mem_usage=True
                )
                self.model = self.model.to(self.device)
            
            logger.info(f"Loaded LLM: {self.model_name} on {self.device}")
        except Exception as e:
            logger.error(f"Error loading LLM {self.model_name}: {str(e)}")
            # Set model to None so we can handle this gracefully
            self.model = None
            self.tokenizer = None
    
    def generate_answer(self, query: str, context: List[Dict[str, Any]]) -> str:
        """
        Generate an answer based on query and context.
        
        Args:
            query: User query
            context: Retrieved context items
            
        Returns:
            Generated answer
        """
        try:
            # Check if model is available
            if self.model is None or self.tokenizer is None:
                # Fallback to simple response with context
                return self._generate_fallback_answer(query, context)
            
            # Format context
            context_text = self._format_context(context)
            
            # Create prompt
            prompt = self._create_prompt(query, context_text)
            
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).to(self.model.device)
            
            # Generate with better parameters
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.max_tokens // 4,  # Limit to avoid overly long responses
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id
                )
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract just the answer part (remove prompt)
            if prompt in answer:
                answer = answer[len(prompt):].strip()
            
            logger.info(f"Generated answer for query: {query} (length: {len(answer)} chars)")
            return answer
        except Exception as e:
            logger.error(f"Error generating answer for query '{query}': {str(e)}")
            # Fallback to simple response with context
            return self._generate_fallback_answer(query, context)
    
    def _generate_fallback_answer(self, query: str, context: List[Dict[str, Any]]) -> str:
        """
        Generate a fallback answer when LLM is not available.
        
        Args:
            query: User query
            context: Retrieved context items
            
        Returns:
            Formatted answer with context
        """
        context_text = self._format_context(context)
        answer = f"I found the following relevant information for your query '{query}':\n\n{context_text}"
        answer += "\n\nNote: The LLM model is not available, so I'm providing the raw context instead of a generated answer."
        return answer
    
    def _format_context(self, context: List[Dict[str, Any]]) -> str:
        """
        Format retrieved context for prompt.
        
        Args:
            context: Retrieved context items
            
        Returns:
            Formatted context string
        """
        formatted_context = []
        for i, item in enumerate(context, 1):
            if item.get('type') == 'text':
                text = item.get('text', '')
                source = item.get('source', 'Unknown')
                page = item.get('page', '')
                paragraph = item.get('paragraph', '')
                
                citation = f"[{i}] {source}"
                if page:
                    citation += f" (Page {page}"
                    if paragraph:
                        citation += f", Paragraph {paragraph}"
                    citation += ")"
                
                formatted_context.append(f"{citation}: {text}")
            elif item.get('type') == 'image':
                source = item.get('source', 'Unknown')
                formatted_context.append(f"[{i}] Image: {source}")
            elif item.get('type') == 'audio':
                source = item.get('source', 'Unknown')
                formatted_context.append(f"[{i}] Audio: {source}")
        
        return "\n\n".join(formatted_context)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """
        Create prompt for the LLM.
        
        Args:
            query: User query
            context: Formatted context
            
        Returns:
            Complete prompt
        """
        prompt = f"""
You are a helpful assistant that answers questions based on provided context. 
Use the following context to answer the question at the end. 
If you don't know the answer, just say that you don't know. 
Use a professional tone and cite sources using the format [number].

Context:
{context}

Question: {query}

Answer:"""
        return prompt.strip()