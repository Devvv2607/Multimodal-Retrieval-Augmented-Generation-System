"""
Debug script to test the ingestion process.
"""

import os
import sys
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_ingestion():
    """Debug the ingestion process."""
    print("Debugging Ingestion Process")
    print("=" * 30)
    
    try:
        # Import components
        print("1. Importing components...")
        from ingestion.ingestor import Ingestor
        from indexing.vector_store import VectorStore
        from utils.config import config
        print("   ✓ Components imported")
        
        # Check sample data file
        sample_file = "./sample_data/ai_overview.txt"
        if os.path.exists(sample_file):
            print(f"2. Sample file exists: {sample_file}")
            # Check file content
            with open(sample_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"   File size: {len(content)} characters")
                print(f"   First 100 chars: {content[:100]}")
        else:
            print(f"2. Sample file does not exist: {sample_file}")
            return False
        
        # Initialize ingestor
        print("3. Initializing ingestor...")
        ingestor = Ingestor()
        print("   ✓ Ingestor initialized")
        
        # Check vector store before ingestion
        print("4. Checking vector store before ingestion...")
        vector_store = VectorStore(
            dimension=config.get('models.text_embedding.dim', 384),
            index_path=config.get('vector_db.index_path'),
            metadata_path=config.get('vector_db.metadata_path')
        )
        initial_count = vector_store.get_total_vectors()
        print(f"   Initial vector count: {initial_count}")
        
        # Process the sample file
        print("5. Processing sample file...")
        result = ingestor._process_file(sample_file)
        print(f"   Processing result: {result}")
        
        # Check vector store after ingestion
        print("6. Checking vector store after ingestion...")
        vector_store = VectorStore(
            dimension=config.get('models.text_embedding.dim', 384),
            index_path=config.get('vector_db.index_path'),
            metadata_path=config.get('vector_db.metadata_path')
        )
        final_count = vector_store.get_total_vectors()
        print(f"   Final vector count: {final_count}")
        print(f"   Vectors added: {final_count - initial_count}")
        
        if final_count > initial_count:
            print("✓ Ingestion successful!")
            return True
        else:
            print("✗ No vectors were added during ingestion")
            return False
        
    except Exception as e:
        print(f"Error during debugging: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_ingestion()
    sys.exit(0 if success else 1)