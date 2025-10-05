"""
Generator for producing answers using the local LLM.
"""

import logging
from typing import List, Dict, Any
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

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
        self._load_model()
    
    def _load_model(self):
        """Load the LLM and tokenizer."""
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map="auto",
                torch_dtype="auto"
            )
            logger.info(f"Loaded LLM: {self.model_name} on {self.device}")
        except Exception as e:
            logger.error(f"Error loading LLM {self.model_name}: {str(e)}")
            raise
    
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
            # Format context
            context_text = self._format_context(context)
            
            # Create prompt
            prompt = self._create_prompt(query, context_text)
            
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            
            # Generate
            outputs = self.model.generate(**inputs, max_new_tokens=250)
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract just the answer part (remove prompt)
            if prompt in answer:
                answer = answer[len(prompt):].strip()
            
            logger.info(f"Generated answer for query: {query}")
            return answer
        except Exception as e:
            logger.error(f"Error generating answer for query '{query}': {str(e)}")
            return "I couldn't generate an answer for that query."
    
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