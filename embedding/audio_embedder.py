"""
Audio embedder for transcribing audio and generating embeddings.
"""

import logging
from typing import List, Dict, Any
import whisper
import torch
import numpy as np

logger = logging.getLogger(__name__)

class AudioEmbedder:
    """Embedder for audio files using Whisper for transcription."""
    
    def __init__(self, model_name: str = "base"):
        """
        Initialize audio embedder.
        
        Args:
            model_name: Name of the Whisper model to use
        """
        self.model_name = model_name
        self.model = None
        self.device = None
        self._load_model()
    
    def _load_model(self):
        """Load the Whisper model."""
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            # Use available models
            available_models = whisper.available_models()
            if self.model_name not in available_models:
                logger.warning(f"Model {self.model_name} not available. Using 'base' instead.")
                self.model_name = "base"
            
            self.model = whisper.load_model(self.model_name, device=self.device)
            logger.info(f"Loaded Whisper audio model: {self.model_name} on {self.device}")
        except Exception as e:
            logger.error(f"Error loading Whisper audio model {self.model_name}: {str(e)}")
            raise
    
    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe an audio file.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary containing transcription and segments
        """
        try:
            # Transcribe audio
            result = self.model.transcribe(audio_path)
            
            logger.info(f"Transcribed audio file: {audio_path}")
            return result
        except Exception as e:
            logger.error(f"Error transcribing audio file {audio_path}: {str(e)}")
            return {}
    
    def embed_audio_text(self, text: str, text_embedder) -> List[float]:
        """
        Generate embedding for transcribed audio text.
        
        Args:
            text: Transcribed text
            text_embedder: TextEmbedder instance to use for embedding
            
        Returns:
            Embedding vector
        """
        try:
            embedding = text_embedder.embed_text(text)
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding for audio text: {str(e)}")
            return []