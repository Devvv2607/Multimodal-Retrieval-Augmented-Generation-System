"""
Script to verify that all modules can be imported correctly.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test importing all modules."""
    modules_to_test = [
        # Utils
        "utils.config",
        "utils.logger",
        
        # Ingestion
        "ingestion.document_processor",
        "ingestion.image_processor",
        "ingestion.audio_processor",
        "ingestion.text_processor",
        "ingestion.ingestor",
        
        # Embedding
        "embedding.text_embedder",
        "embedding.image_embedder",
        "embedding.audio_embedder",
        
        # Indexing
        "indexing.vector_store",
        
        # Retrieval
        "retrieval.retriever",
        
        # Generation
        "generation.generator",
        
        # Query
        "query.cli_interface",
        "query.gui_interface",
        
        # Models
        "models.setup_models",
        
        # Main modules
        "init",
        "main",
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module} - {e}")
            failed_imports.append(module)
        except Exception as e:
            print(f"✗ {module} - {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def main():
    """Main verification function."""
    print("Verifying Multimodal RAG System Installation")
    print("=" * 45)
    
    success = test_imports()
    
    print("\n" + "=" * 45)
    if success:
        print("✓ All modules imported successfully!")
        print("\nNext steps:")
        print("1. Run setup_env.bat (Windows) or setup_env.sh (Unix) to set up the environment")
        print("2. Activate the virtual environment")
        print("3. Run python models/setup_models.py to download models")
        print("4. Run python example_usage.py to see a demonstration")
    else:
        print("✗ Some modules failed to import. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)