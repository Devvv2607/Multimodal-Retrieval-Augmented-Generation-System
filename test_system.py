"""
Test script for the multimodal RAG system.
"""

import os
import sys
import tempfile
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.logger import setup_logger
logger = setup_logger("multimodal_rag_test")

def create_test_files():
    """Create simple test files for system testing."""
    # Create test directory
    test_dir = "./test_files"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create a simple text file
    text_content = """
This is a test document for the multimodal RAG system.
It contains sample text that can be used to test the ingestion and retrieval capabilities.
The system should be able to process this text and generate embeddings for it.
"""
    
    with open(os.path.join(test_dir, "test_document.txt"), "w") as f:
        f.write(text_content)
    
    logger.info(f"Created test files in {test_dir}")
    return test_dir

def test_ingestion():
    """Test the ingestion process."""
    try:
        logger.info("Testing ingestion process...")
        
        # Import ingestor
        from ingestion.ingestor import Ingestor
        
        # Create test files
        test_dir = create_test_files()
        
        # Initialize ingestor
        ingestor = Ingestor()
        
        # Ingest test files
        count = ingestor.ingest_directory(test_dir)
        
        logger.info(f"Ingested {count} test files")
        return count > 0
    except Exception as e:
        logger.error(f"Error in ingestion test: {str(e)}")
        return False

def test_vector_store():
    """Test the vector store."""
    try:
        logger.info("Testing vector store...")
        
        # Import vector store
        from indexing.vector_store import VectorStore
        from utils.config import config
        
        # Initialize vector store
        vector_store = VectorStore(
            dimension=config.get('models.text_embedding.dim', 384),
            index_path=config.get('vector_db.index_path'),
            metadata_path=config.get('vector_db.metadata_path')
        )
        
        # Check if vectors were added
        total_vectors = vector_store.get_total_vectors()
        logger.info(f"Vector store contains {total_vectors} vectors")
        
        return True
    except Exception as e:
        logger.error(f"Error in vector store test: {str(e)}")
        return False

def run_tests():
    """Run all tests for the system."""
    logger.info("Running system tests...")
    
    # Test ingestion
    if not test_ingestion():
        logger.error("Ingestion test failed")
        return False
    
    # Test vector store
    if not test_vector_store():
        logger.error("Vector store test failed")
        return False
    
    logger.info("All tests passed!")
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)