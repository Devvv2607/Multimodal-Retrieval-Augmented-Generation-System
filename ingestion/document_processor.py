"""
Document processor for extracting text from DOCX and PDF files.
"""

import os
from typing import List, Dict, Any
from docx import Document
from PyPDF2 import PdfReader
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Processor for document files (DOCX, PDF)."""
    
    def __init__(self):
        """Initialize document processor."""
        pass
    
    def process_document(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a document file and extract text content.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of text chunks with metadata
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.docx':
            return self._process_docx(file_path)
        elif file_extension == '.pdf':
            return self._process_pdf(file_path)
        else:
            logger.warning(f"Unsupported document format: {file_extension}")
            return []
    
    def _process_docx(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a DOCX file and extract text.
        
        Args:
            file_path: Path to the DOCX file
            
        Returns:
            List of text paragraphs with metadata
        """
        try:
            doc = Document(file_path)
            chunks = []
            
            for i, paragraph in enumerate(doc.paragraphs):
                if paragraph.text.strip():  # Only process non-empty paragraphs
                    chunks.append({
                        'text': paragraph.text.strip(),
                        'source': file_path,
                        'page': 0,  # DOCX doesn't have pages
                        'paragraph': i,
                        'type': 'text'
                    })
            
            logger.info(f"Processed DOCX file: {file_path} ({len(chunks)} paragraphs)")
            return chunks
        except Exception as e:
            logger.error(f"Error processing DOCX file {file_path}: {str(e)}")
            return []
    
    def _process_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a PDF file and extract text.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of text chunks with metadata
        """
        try:
            reader = PdfReader(file_path)
            chunks = []
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text.strip():  # Only process pages with text
                    # Split text into paragraphs
                    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
                    for i, paragraph in enumerate(paragraphs):
                        chunks.append({
                            'text': paragraph,
                            'source': file_path,
                            'page': page_num,
                            'paragraph': i,
                            'type': 'text'
                        })
            
            logger.info(f"Processed PDF file: {file_path} ({len(chunks)} chunks)")
            return chunks
        except Exception as e:
            logger.error(f"Error processing PDF file {file_path}: {str(e)}")
            return []