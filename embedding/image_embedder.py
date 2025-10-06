"""
Image embedder for generating embeddings from images using CLIP.
"""

import logging
from typing import List, Dict, Any
import torch
import numpy as np

# Try to import CLIP, but handle the case where it's not available
try:
    import clip
    CLIP_AVAILABLE = True
except ImportError:
    CLIP_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("CLIP library not available. Image embedding functionality will be disabled.")

if CLIP_AVAILABLE:
    from PIL import Image

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
        
        if CLIP_AVAILABLE:
            self._load_model()
        else:
            logger.warning("CLIP not available. Image embedder initialized in fallback mode.")
    
    def _load_model(self):
        """Load the CLIP model."""
        try:
            if not CLIP_AVAILABLE:
                raise ImportError("CLIP library not available")
                
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
            # Don't raise the exception, just work in fallback mode
            self.model = None
            self.preprocess = None
    
    def embed_images(self, image_paths: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of images.
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            List of embeddings (one for each image)
        """
        # Return empty embeddings if CLIP is not available or model failed to load
        if not CLIP_AVAILABLE or self.model is None or self.preprocess is None:
            logger.warning("CLIP not available or model not loaded. Returning empty embeddings.")
            return [[] for _ in image_paths]
        
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
            # Return empty embeddings as fallback
            return [[] for _ in image_paths]
    
    def embed_image(self, image_path: str) -> List[float]:
        """
        Generate embedding for a single image.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Embedding vector
        """
        # Return empty embedding if CLIP is not available or model failed to load
        if not CLIP_AVAILABLE or self.model is None or self.preprocess is None:
            logger.warning("CLIP not available or model not loaded. Returning empty embedding.")
            return []
        
        embeddings = self.embed_images([image_path])
        return embeddings[0] if embeddings else []