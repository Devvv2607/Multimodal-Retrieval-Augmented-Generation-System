"""
Vector store for managing embeddings in FAISS.
"""

import faiss
import numpy as np
import json
import os
import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

class VectorStore:
    """Vector store using FAISS for efficient similarity search."""
    
    def __init__(self, dimension: int, index_path: str = "./data/index.faiss", 
                 metadata_path: str = "./data/metadata.json"):
        """
        Initialize vector store.
        
        Args:
            dimension: Dimension of the vectors
            index_path: Path to save/load the FAISS index
            metadata_path: Path to save/load metadata
        """
        self.dimension = dimension
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.index = None
        self.metadata = []
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        # Initialize or load the index
        self._init_index()
    
    def _init_index(self):
        """Initialize the FAISS index."""
        try:
            if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
                # Load existing index
                self.index = faiss.read_index(self.index_path)
                
                # Load metadata
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                
                logger.info(f"Loaded existing FAISS index with {self.index.ntotal} vectors")
            else:
                # Create new index
                self.index = faiss.IndexFlatL2(self.dimension)
                self.metadata = []
                logger.info(f"Created new FAISS index with dimension {self.dimension}")
        except Exception as e:
            logger.error(f"Error initializing FAISS index: {str(e)}")
            # Fallback to creating a new index
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []
    
    def add_vectors(self, vectors: List[List[float]], metadata_list: List[Dict[Any, Any]]) -> None:
        """
        Add vectors and their metadata to the index.
        
        Args:
            vectors: List of vectors to add
            metadata_list: List of metadata corresponding to each vector
        """
        try:
            # Convert to numpy array
            vectors_np = np.array(vectors).astype('float32')
            
            # Add to index
            self.index.add(vectors_np)
            
            # Add metadata
            self.metadata.extend(metadata_list)
            
            # Save index and metadata
            self._save_index()
            
            logger.info(f"Added {len(vectors)} vectors to index")
        except Exception as e:
            logger.error(f"Error adding vectors to index: {str(e)}")
    
    def search(self, query_vector: List[float], k: int = 5) -> Tuple[List[int], List[float]]:
        """
        Search for similar vectors.
        
        Args:
            query_vector: Query vector
            k: Number of nearest neighbors to retrieve
            
        Returns:
            Tuple of (indices, distances)
        """
        try:
            # Convert to numpy array
            query_np = np.array([query_vector]).astype('float32')
            
            # Search
            distances, indices = self.index.search(query_np, k)
            
            # Flatten results
            distances = distances[0].tolist()
            indices = indices[0].tolist()
            
            logger.debug(f"Search returned {len(indices)} results")
            return indices, distances
        except Exception as e:
            logger.error(f"Error searching index: {str(e)}")
            return [], []
    
    def get_metadata(self, indices: List[int]) -> List[Dict[Any, Any]]:
        """
        Get metadata for given indices.
        
        Args:
            indices: List of indices
            
        Returns:
            List of metadata dictionaries
        """
        try:
            return [self.metadata[i] for i in indices if i < len(self.metadata)]
        except Exception as e:
            logger.error(f"Error retrieving metadata: {str(e)}")
            return []
    
    def _save_index(self):
        """Save the index and metadata to disk."""
        try:
            # Save FAISS index
            faiss.write_index(self.index, self.index_path)
            
            # Save metadata
            with open(self.metadata_path, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            
            logger.info("Saved FAISS index and metadata")
        except Exception as e:
            logger.error(f"Error saving index: {str(e)}")
    
    def get_total_vectors(self) -> int:
        """
        Get the total number of vectors in the index.
        
        Returns:
            Number of vectors
        """
        return self.index.ntotal if self.index else 0