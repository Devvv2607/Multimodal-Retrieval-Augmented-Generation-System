"""
Image embedder for generating embeddings from images using CLIP.
"""

import logging
from typing import List, Dict, Any
import torch
import clip
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

class ImageEmbedder:
    """Embedder for images using CLIP."""
    
    def __init__(self, model_name: str = "ViT-B/32"):
        """
        Initialize image embedder.
        
        Args:
            model_name: Name of the CLIP model to use
        """
        self.model_name = model_name
        self.model = None
        self.preprocess = None
        self.device = None
        self._load_model()
    
    def _load_model(self):
        """Load the CLIP model."""
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            # Use an available model
            available_models = clip.available_models()
            if self.model_name not in available_models:
                logger.warning(f"Model {self.model_name} not available. Using ViT-B/32 instead.")
                self.model_name = "ViT-B/32"
            
            self.model, self.preprocess = clip.load(self.model_name, device=self.device)
            logger.info(f"Loaded CLIP image embedding model: {self.model_name} on {self.device}")
        except Exception as e:
            logger.error(f"Error loading CLIP image embedding model {self.model_name}: {str(e)}")
            raise
    
    def embed_images(self, image_paths: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of images.
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            List of embeddings (one for each image)
        """
        try:
            images = []
            for path in image_paths:
                image = Image.open(path)
                image = self.preprocess(image).unsqueeze(0).to(self.device)
                images.append(image)
            
            # Stack images into a batch
            image_batch = torch.cat(images)
            
            # Generate embeddings
            with torch.no_grad():
                embeddings = self.model.encode_image(image_batch)
                embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)  # Normalize
                embeddings = embeddings.cpu().numpy()
            
            logger.info(f"Generated embeddings for {len(image_paths)} images")
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating image embeddings: {str(e)}")
            return []
    
    def embed_image(self, image_path: str) -> List[float]:
        """
        Generate embedding for a single image.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Embedding vector
        """
        return self.embed_images([image_path])[0]