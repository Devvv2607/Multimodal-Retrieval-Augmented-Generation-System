"""
Image processor for handling image files and preparing them for embedding.
"""

import os
from typing import List, Dict, Any
from PIL import Image
import logging
import numpy as np

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Processor for image files."""
    
    def __init__(self, target_size: tuple = (224, 224)):
        """
        Initialize image processor.
        
        Args:
            target_size: Target size for image resizing (width, height)
        """
        self.target_size = target_size
    
    def process_image(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process an image file.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            List containing image metadata
        """
        try:
            # Verify it's a valid image file
            with Image.open(file_path) as img:
                img_format = img.format
                img_mode = img.mode
                
            # Return metadata
            result = [{
                'source': file_path,
                'format': img_format,
                'mode': img_mode,
                'size': os.path.getsize(file_path),
                'type': 'image'
            }]
            
            logger.info(f"Processed image file: {file_path}")
            return result
        except Exception as e:
            logger.error(f"Error processing image file {file_path}: {str(e)}")
            return []