"""
Verification script for deployment setup.
This script verifies that the deployment environment is properly configured.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_core_components():
    """Verify that core components can be imported."""
    try:
        from ingestion.ingestor import Ingestor
        from retrieval.retriever import Retriever
        from generation.generator import Generator
        from indexing.vector_store import VectorStore
        from embedding.text_embedder import TextEmbedder
        from utils.config import config
        print("✓ Core components imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Core component import failed: {e}")
        return False

def verify_optional_components():
    """Verify that optional components can be imported."""
    try:
        from embedding.image_embedder import ImageEmbedder
        print("✓ Image embedder imported successfully")
    except ImportError as e:
        print(f"⚠ Image embedder not available: {e}")
    
    try:
        from embedding.audio_embedder import AudioEmbedder
        print("✓ Audio embedder imported successfully")
    except ImportError as e:
        print(f"⚠ Audio embedder not available: {e}")

def verify_streamlit():
    """Verify that Streamlit can be imported."""
    try:
        import streamlit
        print(f"✓ Streamlit version {streamlit.__version__} imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False

def verify_models():
    """Verify that models can be loaded."""
    try:
        from embedding.text_embedder import TextEmbedder
        text_embedder = TextEmbedder()
        print("✓ Text embedder model loaded successfully")
        return True
    except Exception as e:
        print(f"⚠ Text embedder model loading failed: {e}")
        return False

def main():
    """Main verification function."""
    print("Verifying deployment setup...")
    print("=" * 40)
    
    # Verify core components
    core_ok = verify_core_components()
    
    # Verify optional components
    verify_optional_components()
    
    # Verify Streamlit
    streamlit_ok = verify_streamlit()
    
    # Verify models
    models_ok = verify_models()
    
    print("=" * 40)
    
    if core_ok and streamlit_ok:
        print("✅ Deployment setup verification passed!")
        print("The application should run successfully.")
        return True
    else:
        print("❌ Deployment setup verification failed!")
        print("Please check the installation and dependencies.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)