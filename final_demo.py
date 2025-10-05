"""
Final demonstration of the Multimodal RAG System.
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Run final demonstration."""
    print("Multimodal RAG System - Final Demonstration")
    print("=" * 45)
    
    try:
        # Import required components
        from retrieval.retriever import Retriever
        from indexing.vector_store import VectorStore
        from embedding.text_embedder import TextEmbedder
        from embedding.image_embedder import ImageEmbedder
        from utils.config import config
        
        # Initialize components
        print("1. Initializing system components...")
        vector_store = VectorStore(
            dimension=config.get('models.text_embedding.dim', 384),
            index_path=config.get('vector_db.index_path'),
            metadata_path=config.get('vector_db.metadata_path')
        )
        
        text_embedder = TextEmbedder(config.get('models.text_embedding.name'))
        image_embedder = ImageEmbedder(config.get('models.image_embedding.name'))
        retriever = Retriever(vector_store, text_embedder, image_embedder)
        print("   ✓ Components initialized successfully")
        
        # Check system status
        print("\n2. System Status:")
        total_vectors = vector_store.get_total_vectors()
        print(f"   Indexed vectors: {total_vectors}")
        print(f"   Index path: {config.get('vector_db.index_path')}")
        print(f"   Metadata path: {config.get('vector_db.metadata_path')}")
        
        # Demonstrate retrieval
        print("\n3. Demonstrating retrieval capability:")
        test_queries = [
            "What are the main types of machine learning?",
            "How has AI evolved in recent years?",
            "What is the significance of transformer architectures?"
        ]
        
        for query in test_queries:
            print(f"\n   Query: {query}")
            context = retriever.retrieve_text(query, k=2)
            print(f"   Retrieved {len(context)} relevant items:")
            
            for i, item in enumerate(context, 1):
                # Show a snippet of the text and the source
                text = item.get('text', '')
                source = os.path.basename(item.get('source', 'Unknown'))
                text_snippet = text[:80] + "..." if len(text) > 80 else text
                print(f"     {i}. {text_snippet}")
                print(f"        Source: {source}")
        
        print("\n" + "=" * 45)
        print("✅ Final demonstration completed successfully!")
        print("\nSystem is ready for use with the following commands:")
        print("  python main.py ingest --input_dir <directory>")
        print("  python main.py query --question \"Your question here\"")
        print("  python main.py status")
        print("  python main.py --gui")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)