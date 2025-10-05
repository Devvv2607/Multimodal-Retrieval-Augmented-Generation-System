"""
Minimal test to verify the RAG system is working correctly.
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_system():
    """Test the system components."""
    print("Testing Multimodal RAG System Components")
    print("=" * 40)
    
    try:
        # Test 1: Import all components
        print("1. Testing component imports...")
        from ingestion.ingestor import Ingestor
        from retrieval.retriever import Retriever
        from generation.generator import Generator
        from indexing.vector_store import VectorStore
        from embedding.text_embedder import TextEmbedder
        from embedding.image_embedder import ImageEmbedder
        from utils.config import config
        print("   ✓ All components imported successfully")
        
        # Test 2: Initialize components
        print("2. Testing component initialization...")
        vector_store = VectorStore(
            dimension=config.get('models.text_embedding.dim', 384),
            index_path=config.get('vector_db.index_path'),
            metadata_path=config.get('vector_db.metadata_path')
        )
        text_embedder = TextEmbedder(config.get('models.text_embedding.name'))
        image_embedder = ImageEmbedder(config.get('models.image_embedding.name'))
        retriever = Retriever(vector_store, text_embedder, image_embedder)
        print("   ✓ All components initialized successfully")
        
        # Test 3: Check vector store
        print("3. Testing vector store...")
        total_vectors = vector_store.get_total_vectors()
        print(f"   ✓ Vector store contains {total_vectors} vectors")
        
        # Test 4: Test retrieval
        print("4. Testing retrieval...")
        query = "What is machine learning?"
        context = retriever.retrieve_text(query, k=2)
        print(f"   ✓ Retrieved {len(context)} items for query: '{query}'")
        
        if context:
            print("   Sample retrieved content:")
            for i, item in enumerate(context[:2]):
                text = item.get('text', '')[:100] + "..." if len(item.get('text', '')) > 100 else item.get('text', '')
                source = os.path.basename(item.get('source', 'Unknown'))
                print(f"     {i+1}. {text} (Source: {source})")
        
        print("\nAll tests passed! The system is working correctly.")
        return True
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)