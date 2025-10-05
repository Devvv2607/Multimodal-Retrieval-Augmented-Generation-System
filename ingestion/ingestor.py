"""
Main ingestor that coordinates the ingestion of multimodal content.
"""

import os
import logging
from typing import List, Dict, Any
from ingestion.document_processor import DocumentProcessor
from ingestion.image_processor import ImageProcessor
from ingestion.audio_processor import AudioProcessor
from ingestion.text_processor import TextProcessor
from embedding.text_embedder import TextEmbedder
from embedding.image_embedder import ImageEmbedder
from embedding.audio_embedder import AudioEmbedder
from indexing.vector_store import VectorStore
from utils.config import config

logger = logging.getLogger(__name__)

class Ingestor:
    """Main ingestor for multimodal content."""
    
    def __init__(self):
        """Initialize ingestor with all processors and embedders."""
        # Initialize processors
        self.document_processor = DocumentProcessor()
        self.image_processor = ImageProcessor(
            target_size=tuple(config.get('processing.image_size', [224, 224]))
        )
        self.audio_processor = AudioProcessor()
        self.text_processor = TextProcessor(
            chunk_size=config.get('processing.chunk_size', 512),
            chunk_overlap=config.get('processing.chunk_overlap', 50)
        )
        
        # Initialize embedders
        self.text_embedder = TextEmbedder(config.get('models.text_embedding.name'))
        self.image_embedder = ImageEmbedder(config.get('models.image_embedding.name'))
        self.audio_embedder = AudioEmbedder(config.get('models.audio_embedding.name', 'base'))
        
        # Initialize vector store
        self.vector_store = VectorStore(
            dimension=config.get('models.text_embedding.dim', 384),
            index_path=config.get('vector_db.index_path'),
            metadata_path=config.get('vector_db.metadata_path')
        )
        
        # Supported file extensions
        self.supported_extensions = {
            'document': ['.docx', '.pdf'],
            'image': ['.png', '.jpg', '.jpeg', '.bmp', '.tiff'],
            'audio': ['.mp3', '.wav', '.flac', '.m4a'],
            'text': ['.txt']
        }
    
    def ingest_directory(self, directory_path: str, recursive: bool = False) -> int:
        """
        Ingest all supported files in a directory.
        
        Args:
            directory_path: Path to directory containing files to ingest
            recursive: Whether to process subdirectories recursively
            
        Returns:
            Number of files processed
        """
        processed_count = 0
        
        try:
            if recursive:
                for root, dirs, files in os.walk(directory_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if self._process_file(file_path):
                            processed_count += 1
            else:
                for file in os.listdir(directory_path):
                    file_path = os.path.join(directory_path, file)
                    if os.path.isfile(file_path) and self._process_file(file_path):
                        processed_count += 1
            
            logger.info(f"Ingested {processed_count} files from {directory_path}")
            return processed_count
        except Exception as e:
            logger.error(f"Error ingesting directory {directory_path}: {str(e)}")
            return processed_count
    
    def _process_file(self, file_path: str) -> bool:
        """
        Process a single file based on its extension.
        
        Args:
            file_path: Path to file to process
            
        Returns:
            True if file was processed successfully, False otherwise
        """
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            # Determine file type and process accordingly
            if file_extension in self.supported_extensions['document']:
                return self._process_document(file_path)
            elif file_extension in self.supported_extensions['image']:
                return self._process_image(file_path)
            elif file_extension in self.supported_extensions['audio']:
                return self._process_audio(file_path)
            elif file_extension in self.supported_extensions['text']:
                return self._process_text(file_path)
            else:
                logger.debug(f"Unsupported file type: {file_extension}")
                return False
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return False
    
    def _process_document(self, file_path: str) -> bool:
        """
        Process a document file.
        
        Args:
            file_path: Path to document file
            
        Returns:
            True if processed successfully
        """
        try:
            # Extract text
            chunks = self.document_processor.process_document(file_path)
            
            if not chunks:
                return False
            
            # Extract texts for embedding
            texts = [chunk['text'] for chunk in chunks if 'text' in chunk]
            
            if not texts:
                return False
            
            # Generate embeddings
            embeddings = self.text_embedder.embed_texts(texts)
            
            # Add to vector store
            self.vector_store.add_vectors(embeddings, chunks)
            
            return True
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {str(e)}")
            return False
    
    def _process_image(self, file_path: str) -> bool:
        """
        Process an image file.
        
        Args:
            file_path: Path to image file
            
        Returns:
            True if processed successfully
        """
        try:
            # Process image metadata
            metadata = self.image_processor.process_image(file_path)
            
            if not metadata:
                return False
            
            # Generate embedding
            embedding = self.image_embedder.embed_image(file_path)
            
            # Add to vector store
            self.vector_store.add_vectors([embedding], metadata)
            
            return True
        except Exception as e:
            logger.error(f"Error processing image {file_path}: {str(e)}")
            return False
    
    def _process_audio(self, file_path: str) -> bool:
        """
        Process an audio file.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            True if processed successfully
        """
        try:
            # Process audio metadata
            metadata = self.audio_processor.process_audio(file_path)
            
            if not metadata:
                return False
            
            # Transcribe audio
            transcription_result = self.audio_embedder.transcribe_audio(file_path)
            transcript = transcription_result.get('text', '')
            
            if not transcript:
                # Add metadata only if no transcript
                self.vector_store.add_vectors([[0.0] * config.get('models.text_embedding.dim', 384)], metadata)
                return True
            
            # Generate embedding for transcript
            embedding = self.audio_embedder.embed_audio_text(transcript, self.text_embedder)
            
            # Update metadata with transcription info
            metadata[0]['transcript'] = transcript
            metadata[0]['segments'] = transcription_result.get('segments', [])
            
            # Add to vector store
            self.vector_store.add_vectors([embedding], metadata)
            
            return True
        except Exception as e:
            logger.error(f"Error processing audio {file_path}: {str(e)}")
            return False
    
    def _process_text(self, file_path: str) -> bool:
        """
        Process a text file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            True if processed successfully
        """
        try:
            # Extract text chunks
            chunks = self.text_processor.process_text(file_path)
            
            if not chunks:
                return False
            
            # Extract texts for embedding
            texts = [chunk['text'] for chunk in chunks if 'text' in chunk]
            
            if not texts:
                return False
            
            # Generate embeddings
            embeddings = self.text_embedder.embed_texts(texts)
            
            # Add to vector store
            self.vector_store.add_vectors(embeddings, chunks)
            
            return True
        except Exception as e:
            logger.error(f"Error processing text {file_path}: {str(e)}")
            return False