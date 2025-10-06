"""
Retriever for finding relevant content based on queries.
"""

import logging
from typing import List, Dict, Any, Tuple
from indexing.vector_store import VectorStore
from embedding.text_embedder import TextEmbedder
from embedding.image_embedder import ImageEmbedder
import numpy as np

logger = logging.getLogger(__name__)

class Retriever:
    """Retriever for multimodal content."""
    
    def __init__(self, vector_store: VectorStore, text_embedder: TextEmbedder, 
                 image_embedder: ImageEmbedder):
        """
        Initialize retriever.
        
        Args:
            vector_store: Vector store instance
            text_embedder: Text embedder instance
            image_embedder: Image embedder instance
        """
        self.vector_store = vector_store
        self.text_embedder = text_embedder
        self.image_embedder = image_embedder
    
    def retrieve_text(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve text content based on text query.
        
        Args:
            query: Text query
            k: Number of results to retrieve
            
        Returns:
            List of retrieved text items with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.text_embedder.embed_text(query)
            
            # Check if embedding is valid
            if not query_embedding:
                logger.warning("Text embedder returned empty embedding")
                return []
            
            # Search vector store
            indices, distances = self.vector_store.search(query_embedding, k)
            
            # Get metadata
            results = self.vector_store.get_metadata(indices)
            
            # Add distances to results
            for i, result in enumerate(results):
                result['distance'] = distances[i] if i < len(distances) else 0
                # Avoid division by zero
                if distances:
                    result['relevance_score'] = 1 - (distances[i] / np.max(distances)) if np.max(distances) > 0 else 0
                else:
                    result['relevance_score'] = 0
            
            logger.info(f"Retrieved {len(results)} text items for query: {query}")
            return results
        except Exception as e:
            logger.error(f"Error retrieving text for query '{query}': {str(e)}")
            return []
    
    def retrieve_image(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve images based on text query.
        
        Args:
            query: Text query
            k: Number of results to retrieve
            
        Returns:
            List of retrieved images with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.text_embedder.embed_text(query)
            
            # Check if embedding is valid
            if not query_embedding:
                logger.warning("Text embedder returned empty embedding")
                return []
            
            # Search vector store
            indices, distances = self.vector_store.search(query_embedding, k)
            
            # Filter for image results
            all_metadata = self.vector_store.get_metadata(indices)
            image_results = [meta for meta in all_metadata if meta.get('type') == 'image']
            
            # Add distances to results
            for i, result in enumerate(image_results):
                result['distance'] = distances[i] if i < len(distances) else 0
                # Avoid division by zero
                if distances:
                    result['relevance_score'] = 1 - (distances[i] / np.max(distances)) if np.max(distances) > 0 else 0
                else:
                    result['relevance_score'] = 0
            
            logger.info(f"Retrieved {len(image_results)} images for query: {query}")
            return image_results
        except Exception as e:
            logger.error(f"Error retrieving images for query '{query}': {str(e)}")
            return []
    
    def retrieve_by_image(self, image_path: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve content based on image query.
        
        Args:
            image_path: Path to query image
            k: Number of results to retrieve
            
        Returns:
            List of retrieved items with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.image_embedder.embed_image(image_path)
            
            # Check if embedding is valid
            if not query_embedding:
                logger.warning("Image embedder returned empty embedding")
                return []
            
            # Search vector store
            indices, distances = self.vector_store.search(query_embedding, k)
            
            # Get metadata
            results = self.vector_store.get_metadata(indices)
            
            # Add distances to results
            for i, result in enumerate(results):
                result['distance'] = distances[i] if i < len(distances) else 0
                # Avoid division by zero
                if distances:
                    result['relevance_score'] = 1 - (distances[i] / np.max(distances)) if np.max(distances) > 0 else 0
                else:
                    result['relevance_score'] = 0
            
            logger.info(f"Retrieved {len(results)} items for image query: {image_path}")
            return results
        except Exception as e:
            logger.error(f"Error retrieving content for image query '{image_path}': {str(e)}")
            return []