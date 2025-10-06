"""
Deployment script for Streamlit Cloud.
This script handles dependency checking and graceful degradation.
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import core components
try:
    from ingestion.ingestor import Ingestor
    from retrieval.retriever import Retriever
    from generation.generator import Generator
    from indexing.vector_store import VectorStore
    from embedding.text_embedder import TextEmbedder
    from utils.config import config
    CORE_IMPORTS_AVAILABLE = True
except ImportError as e:
    st.error(f"Core imports failed: {e}")
    CORE_IMPORTS_AVAILABLE = False

# Import optional components with graceful fallback
try:
    from embedding.image_embedder import ImageEmbedder
    IMAGE_EMBEDDER_AVAILABLE = True
except ImportError:
    ImageEmbedder = None
    IMAGE_EMBEDDER_AVAILABLE = False
    st.warning("Image processing not available (CLIP not installed)")

try:
    from embedding.audio_embedder import AudioEmbedder
    AUDIO_EMBEDDER_AVAILABLE = True
except ImportError:
    AudioEmbedder = None
    AUDIO_EMBEDDER_AVAILABLE = False
    st.warning("Audio processing not available (Whisper not installed)")

def check_system_status():
    """Check system status and show available features."""
    st.sidebar.header("System Status")
    
    if CORE_IMPORTS_AVAILABLE:
        st.sidebar.success("✅ Core system ready")
    else:
        st.sidebar.error("❌ Core system not available")
    
    if IMAGE_EMBEDDER_AVAILABLE:
        st.sidebar.success("✅ Image processing available")
    else:
        st.sidebar.info("ℹ️ Image processing not available")
    
    if AUDIO_EMBEDDER_AVAILABLE:
        st.sidebar.success("✅ Audio processing available")
    else:
        st.sidebar.info("ℹ️ Audio processing not available")

def main():
    """Main deployment application."""
    st.set_page_config(
        page_title="Multimodal RAG System",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Multimodal Retrieval-Augmented Generation System")
    
    # Check system status
    check_system_status()
    
    if not CORE_IMPORTS_AVAILABLE:
        st.error("The system cannot start due to missing core dependencies.")
        st.info("Please check the installation instructions in the README.")
        return
    
    st.markdown("""
    This system can process documents, images, and audio files to provide intelligent search 
    and question answering capabilities.
    
    ### Supported Features:
    """)
    
    features = []
    features.append("📄 **Text Processing**: Process TXT, DOCX, and PDF documents")
    features.append("💬 **Question Answering**: Ask questions about your indexed content")
    features.append("🔍 **Semantic Search**: Find relevant content using natural language")
    
    if IMAGE_EMBEDDER_AVAILABLE:
        features.append("🖼️ **Image Processing**: Process PNG, JPG, and JPEG images")
    
    if AUDIO_EMBEDDER_AVAILABLE:
        features.append("🔊 **Audio Processing**: Process MP3 and WAV audio files")
    
    for feature in features:
        st.markdown(feature)
    
    st.markdown("""
    ### Getting Started:
    1. Go to the **Ingest** tab to upload and process your files
    2. Use the **Chat** tab to ask questions about your content
    3. Check the **Status** tab to see system information
    """)

if __name__ == "__main__":
    main()