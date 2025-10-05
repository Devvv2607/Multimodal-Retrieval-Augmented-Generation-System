"""
Test script to verify the querying functionality of the RAG system.
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_query():
    """Test the query functionality."""
    print("Testing Query Functionality")
    print("=" * 30)
    
    try:
        # Import required components
        from retrieval.retriever import Retriever
        from generation.generator import Generator
        from indexing.vector_store import VectorStore
        from embedding.text_embedder import TextEmbedder
        from embedding.image_embedder import ImageEmbedder
        from utils.config import config
        
        # Initialize components
        vector_store = VectorStore(
            dimension=config.get('models.text_embedding.dim', 384),
            index_path=config.get('vector_db.index_path'),
            metadata_path=config.get('vector_db.metadata_path')
        )
        
        text_embedder = TextEmbedder(config.get('models.text_embedding.name'))
        image_embedder = ImageEmbedder(config.get('models.image_embedding.name'))
        retriever = Retriever(vector_store, text_embedder, image_embedder)
        
        # Test queries
        test_queries = [
            "What is machine learning?",
            "What are the types of machine learning?",
            "How has AI evolved in recent years?"
        ]
        
        print(f"Total vectors in index: {vector_store.get_total_vectors()}")
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            
            # Retrieve context
            context = retriever.retrieve_text(query, k=3)
            
            print(f"Retrieved {len(context)} results:")
            for i, item in enumerate(context, 1):
                text = item.get('text', '')[:100] + "..." if len(item.get('text', '')) > 100 else item.get('text', '')
                source = os.path.basename(item.get('source', 'Unknown'))
                print(f"  {i}. {text} (Source: {source})")
        
        print("\nQuery testing completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during query testing: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_query()
    sys.exit(0 if success else 1)