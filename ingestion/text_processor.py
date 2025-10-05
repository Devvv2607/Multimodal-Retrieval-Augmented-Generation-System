"""
Text processor for handling plain text files and free-form notes.
"""

import os
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    """Processor for plain text files."""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """
        Initialize text processor.
        
        Args:
            chunk_size: Maximum size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def process_text(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a text file.
        
        Args:
            file_path: Path to the text file
            
        Returns:
            List of text chunks with metadata
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Chunk the text
            chunks = self._chunk_text(content)
            
            # Add metadata
            result = []
            for i, chunk in enumerate(chunks):
                result.append({
                    'text': chunk,
                    'source': file_path,
                    'chunk': i,
                    'type': 'text'
                })
            
            logger.info(f"Processed text file: {file_path} ({len(result)} chunks)")
            return result
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {str(e)}")
            return []
    
    def _chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks.
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start >= len(text):
                break
                
            # Ensure we don't create empty chunks
            if start + self.chunk_size > len(text):
                # If remaining text is small, add it as final chunk
                if len(text) - start > 0:
                    chunks.append(text[start:])
                break
        
        return chunks