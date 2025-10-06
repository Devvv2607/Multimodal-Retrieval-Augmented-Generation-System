"""
Streamlit application for the Multimodal RAG System.
"""

import streamlit as st
import os
import sys
import tempfile
import pandas as pd
from typing import List, Dict, Any
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our RAG system components with error handling
try:
    from ingestion.ingestor import Ingestor
    from retrieval.retriever import Retriever
    from generation.generator import Generator
    from indexing.vector_store import VectorStore
    from embedding.text_embedder import TextEmbedder
    IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.error(f"Import error: {str(e)}")
    IMPORTS_AVAILABLE = False

# Only import embedders if available
if IMPORTS_AVAILABLE:
    try:
        from embedding.image_embedder import ImageEmbedder
    except ImportError:
        ImageEmbedder = None
        logger.warning("ImageEmbedder not available")
    
    try:
        from embedding.audio_embedder import AudioEmbedder
    except ImportError:
        AudioEmbedder = None
        logger.warning("AudioEmbedder not available")

from utils.config import config

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'retriever' not in st.session_state:
    st.session_state.retriever = None
if 'generator' not in st.session_state:
    st.session_state.generator = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'diagnostics' not in st.session_state:
    st.session_state.diagnostics = []

def log_diagnostic(message):
    """Log diagnostic information."""
    st.session_state.diagnostics.append(message)
    logger.info(message)

def initialize_system():
    """Initialize the RAG system components."""
    if not IMPORTS_AVAILABLE:
        st.error("Required dependencies are not available. Please check the installation.")
        return False
        
    try:
        log_diagnostic("Initializing system components...")
        
        # Initialize components
        st.session_state.vector_store = VectorStore(
            dimension=config.get('models.text_embedding.dim', 384),
            index_path=config.get('vector_db.index_path'),
            metadata_path=config.get('vector_db.metadata_path')
        )
        log_diagnostic("Vector store initialized")
        
        text_embedder = TextEmbedder(config.get('models.text_embedding.name'))
        log_diagnostic("Text embedder initialized")
        
        # Initialize image embedder if available
        image_embedder = None
        if ImageEmbedder:
            image_embedder = ImageEmbedder(config.get('models.image_embedding.name'))
            log_diagnostic("Image embedder initialized")
        else:
            log_diagnostic("Image embedder not available")
        
        st.session_state.retriever = Retriever(
            st.session_state.vector_store, 
            text_embedder, 
            image_embedder
        )
        log_diagnostic("Retriever initialized")
        
        # Check if GPU should be used
        use_gpu = config.get('performance.use_gpu', True)
        
        st.session_state.generator = Generator(
            model_name=config.get('models.llm.name'),
            max_tokens=config.get('models.llm.max_tokens', 2048)
        )
        
        # Log GPU status
        if hasattr(st.session_state.generator, 'device'):
            log_diagnostic(f"Model loaded on device: {st.session_state.generator.device}")
            if 'cuda' in str(st.session_state.generator.device):
                try:
                    import torch
                    gpu_name = torch.cuda.get_device_name(0)
                    log_diagnostic(f"Using GPU: {gpu_name}")
                except Exception as gpu_error:
                    log_diagnostic(f"GPU info error: {str(gpu_error)}")
        log_diagnostic("Generator initialized")
        
        if st.session_state.generator.model is not None:
            log_diagnostic("LLM model loaded successfully")
        else:
            log_diagnostic("LLM model not loaded - using fallback mode")
        
        st.session_state.initialized = True
        log_diagnostic("System initialization complete")
        return True
    except Exception as e:
        error_msg = f"Error initializing system: {str(e)}"
        log_diagnostic(error_msg)
        st.error(error_msg)
        return False

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Multimodal RAG System",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Multimodal Retrieval-Augmented Generation System")
    st.markdown("""
    This system can process documents, images, and audio files to provide intelligent search 
    and question answering capabilities. Upload your files and ask questions!
    """)
    
    # Show warning if imports are not available
    if not IMPORTS_AVAILABLE:
        st.warning("Some dependencies are not available. The system may have limited functionality.")
        st.info("Please check that all required packages are installed correctly.")
        return
    
    # Initialize system if not already done
    if 'initialized' not in st.session_state or not st.session_state.initialized:
        with st.spinner("Initializing system..."):
            if not initialize_system():
                st.error("Failed to initialize the system. Please check the logs.")
                return
    
    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📁 Ingest", "💬 Chat", "📊 Status", "🔧 Diagnostics", "ℹ️ About"])
    
    with tab1:
        st.header("Document Ingestion")
        st.markdown("Upload documents to be processed and indexed by the system.")
        
        uploaded_files = st.file_uploader(
            "Choose files to ingest",
            accept_multiple_files=True,
            type=["txt", "docx", "pdf", "png", "jpg", "jpeg", "mp3", "wav"]
        )
        
        if uploaded_files:
            st.info(f"Selected {len(uploaded_files)} files for ingestion.")
            
            if st.button("Process Files"):
                with st.spinner("Processing files..."):
                    try:
                        log_diagnostic(f"Processing {len(uploaded_files)} files")
                        
                        # Create temporary directory for uploaded files
                        with tempfile.TemporaryDirectory() as temp_dir:
                            # Save uploaded files to temporary directory
                            file_paths = []
                            for uploaded_file in uploaded_files:
                                file_path = os.path.join(temp_dir, uploaded_file.name)
                                with open(file_path, "wb") as f:
                                    f.write(uploaded_file.getbuffer())
                                file_paths.append(file_path)
                                log_diagnostic(f"Saved file: {file_path}")
                            
                            # Initialize ingestor with the session state vector store
                            ingestor = Ingestor()
                            # Replace the ingestor's vector store with the session state one
                            ingestor.vector_store = st.session_state.vector_store
                            log_diagnostic("Ingestor initialized with session vector store")
                            
                            # Process each file
                            processed_count = 0
                            for file_path in file_paths:
                                log_diagnostic(f"Processing file: {file_path}")
                                if ingestor._process_file(file_path):
                                    processed_count += 1
                                    log_diagnostic(f"Successfully processed: {file_path}")
                                else:
                                    log_diagnostic(f"Failed to process: {file_path}")
                            
                            st.success(f"Successfully processed {processed_count} out of {len(uploaded_files)} files!")
                            log_diagnostic(f"Processing complete: {processed_count}/{len(uploaded_files)} files processed")
                            
                            # Show system status
                            total_vectors = st.session_state.vector_store.get_total_vectors()
                            st.info(f"Total indexed vectors: {total_vectors}")
                            log_diagnostic(f"Total vectors after processing: {total_vectors}")
                            
                    except Exception as e:
                        error_msg = f"Error processing files: {str(e)}"
                        st.error(error_msg)
                        log_diagnostic(error_msg)
        
        st.markdown("### Supported File Types")
        st.markdown("""
        - **Text Documents**: .txt
        - **Word Documents**: .docx
        - **PDF Documents**: .pdf
        - **Images**: .png, .jpg, .jpeg
        - **Audio**: .mp3, .wav
        """)
    
    with tab2:
        st.header("Chat Interface")
        st.markdown("Ask questions about your indexed content.")
        
        # Add search bar at the top of the chat interface
        with st.container():
            st.markdown("""
            <style>
            .search-container {
                position: sticky;
                top: 0;
                background-color: white;
                padding: 1rem 0;
                border-bottom: 1px solid #e0e0e0;
                z-index: 999;
                margin-bottom: 1rem;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="search-container">', unsafe_allow_html=True)
            col1, col2 = st.columns([4, 1])
            with col1:
                search_query = st.text_input("🔍 Quick Search", 
                                           placeholder="Search through your indexed content...",
                                           key="chat_search")
            with col2:
                search_button = st.button("Search", key="chat_search_button", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Handle search functionality
            if search_button and search_query:
                if st.session_state.initialized and st.session_state.retriever:
                    with st.spinner("Searching..."):
                        try:
                            # Use the retriever to search for relevant content
                            search_results = st.session_state.retriever.retrieve_text(search_query, k=5)
                            
                            if search_results:
                                st.subheader("Search Results")
                                for i, item in enumerate(search_results, 1):
                                    source = os.path.basename(item.get('source', 'Unknown'))
                                    item_type = item.get('type', 'unknown')
                                    
                                    if item_type == 'text':
                                        text = item.get('text', '')[:300] + "..." if len(item.get('text', '')) > 300 else item.get('text', '')
                                        st.markdown(f"**{i}.** {text} \n\n*Source: {source}*")
                                    elif item_type == 'image':
                                        st.markdown(f"**{i}.** Image: {source}")
                                    elif item_type == 'audio':
                                        st.markdown(f"**{i}.** Audio: {source}")
                            else:
                                st.info("No results found for your query.")
                        except Exception as e:
                            st.error(f"Error performing search: {str(e)}")
                            log_diagnostic(f"Error performing search: {str(e)}")
                else:
                    st.warning("System not initialized. Please wait for initialization to complete.")
            
            st.markdown("---")
        
        # Display chat history
        if 'chat_history' in st.session_state:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            # Add user message to chat history
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            log_diagnostic(f"User query: {prompt}")
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Process the query
            with st.chat_message("assistant"):
                status_placeholder = st.empty()
                status_placeholder.markdown("🔍 Retrieving relevant information...")
                
                try:
                    log_diagnostic("Starting retrieval process")
                    
                    # Retrieve context
                    context = st.session_state.retriever.retrieve_text(prompt, k=5)
                    log_diagnostic(f"Retrieved {len(context)} results")
                    
                    status_placeholder.markdown("🧠 Generating answer...")
                    
                    if context:
                        # Display diagnostic info
                        st.markdown(f"**Diagnostic**: Retrieved {len(context)} relevant items")
                        
                        # Generate answer
                        answer_displayed = False
                        response_content = ""
                        if st.session_state.generator.model is not None:
                            log_diagnostic("Generating answer with LLM")
                            try:
                                answer = st.session_state.generator.generate_answer(prompt, context)
                                status_placeholder.empty()  # Clear the status message
                                st.markdown("**Answer:**")
                                st.markdown(answer)
                                answer_displayed = True
                                response_content = f"**Answer:**\n{answer}"
                                log_diagnostic("Answer generated and displayed successfully")
                                log_diagnostic(f"Generated answer length: {len(answer)} characters")
                            except Exception as gen_error:
                                log_diagnostic(f"Error generating answer: {str(gen_error)}")
                                status_placeholder.empty()
                                st.error(f"Error generating answer: {str(gen_error)}")
                                response_content = f"Error generating answer: {str(gen_error)}"
                        else:
                            # Fallback when LLM is not available
                            status_placeholder.empty()  # Clear the status message
                            st.markdown("**Note:** The LLM model is not available. Here's the relevant context I found:")
                            response_content = "**Note:** The LLM model is not available. Here's the relevant context I found:\n\n"
                            for i, item in enumerate(context, 1):
                                source = os.path.basename(item.get('source', 'Unknown'))
                                item_type = item.get('type', 'unknown')
                                
                                if item_type == 'text':
                                    text = item.get('text', '')[:200] + "..." if len(item.get('text', '')) > 200 else item.get('text', '')
                                    st.markdown(f"**{i}.** {text} \n\n*Source: {source}*")
                                    response_content += f"**{i}.** {text} \n\n*Source: {source}*\n\n"
                                elif item_type == 'image':
                                    st.markdown(f"**{i}.** Image: {source}")
                                    response_content += f"**{i}.** Image: {source}\n\n"
                                elif item_type == 'audio':
                                    st.markdown(f"**{i}.** Audio: {source}")
                                    response_content += f"**{i}.** Audio: {source}\n\n"
                            answer_displayed = True
                            log_diagnostic("Showing fallback context")
                        
                        # Always display sources if we have context
                        if context:
                            with st.expander("Sources", expanded=True):
                                for i, item in enumerate(context, 1):
                                    source = os.path.basename(item.get('source', 'Unknown'))
                                    item_type = item.get('type', 'unknown')
                                    
                                    if item_type == 'text':
                                        text = item.get('text', '')[:100] + "..." if len(item.get('text', '')) > 100 else item.get('text', '')
                                        st.markdown(f"**{i}.** {text} \n\n*Source: {source}*")
                                    elif item_type == 'image':
                                        st.markdown(f"**{i}.** Image: {source}")
                                    elif item_type == 'audio':
                                        st.markdown(f"**{i}.** Audio: {source}")
                        
                        # If no answer was displayed for some reason, show a message
                        if not answer_displayed:
                            status_placeholder.empty()
                            st.markdown("I processed your query but couldn't generate a response. Please check the diagnostics tab for more information.")
                    else:
                        status_placeholder.empty()  # Clear the status message
                        st.markdown("I couldn't find any relevant information to answer your question.")
                        log_diagnostic("No relevant context found")
                        
                    # Add assistant response to chat history
                    if not response_content:
                        response_content = "I couldn't find any relevant information to answer your question."
                        if context:
                            if st.session_state.generator.model is not None:
                                try:
                                    response_content = st.session_state.generator.generate_answer(prompt, context)
                                except Exception as gen_error:
                                    response_content = f"Error generating answer: {str(gen_error)}"
                            else:
                                response_content = "I found relevant context but the LLM model is not available to generate a response."
                    
                    # Add to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": response_content})
                    log_diagnostic("Response added to chat history")
                    
                except Exception as e:
                    status_placeholder.empty()  # Clear the status message
                    error_msg = f"Error processing query: {str(e)}"
                    st.error(error_msg)
                    log_diagnostic(error_msg)
                    if 'chat_history' in st.session_state:
                        st.session_state.chat_history.append({"role": "assistant", "content": f"Error: {str(e)}"})
    
    with tab3:
        st.header("System Status")
        
        if 'initialized' in st.session_state and st.session_state.initialized:
            total_vectors = st.session_state.vector_store.get_total_vectors()
            st.metric("Indexed Vectors", total_vectors)
            
            # Show index path
            st.subheader("Configuration")
            st.text(f"Index Path: {config.get('vector_db.index_path')}")
            st.text(f"Metadata Path: {config.get('vector_db.metadata_path')}")
            
            # Show models
            st.subheader("Models")
            st.text(f"Text Embedding: {config.get('models.text_embedding.name')}")
            if ImageEmbedder:
                st.text(f"Image Embedding: {config.get('models.image_embedding.name')}")
            else:
                st.text("Image Embedding: Not available")
            st.text(f"LLM: {config.get('models.llm.name')}")
            
            # Show LLM status
            if st.session_state.generator.model is not None:
                st.success("✅ LLM Model: Loaded successfully")
            else:
                st.warning("⚠️ LLM Model: Not available (using fallback mode)")
            
            # Show metadata if available
            if total_vectors > 0:
                st.subheader("Indexed Content")
                try:
                    # Load metadata
                    import json
                    with open(config.get('vector_db.metadata_path'), 'r') as f:
                        metadata = json.load(f)
                    
                    # Create a summary
                    content_types = {}
                    sources = set()
                    for item in metadata:
                        item_type = item.get('type', 'unknown')
                        content_types[item_type] = content_types.get(item_type, 0) + 1
                        sources.add(os.path.basename(item.get('source', 'Unknown')))
                    
                    # Display summary
                    st.markdown("#### Content Summary")
                    for content_type, count in content_types.items():
                        st.text(f"{content_type.capitalize()}: {count} items")
                    
                    st.markdown("#### Indexed Sources")
                    for source in list(sources)[:10]:  # Show first 10 sources
                        st.text(f"• {source}")
                    
                    if len(sources) > 10:
                        st.text(f"... and {len(sources) - 10} more")
                        
                except Exception as e:
                    st.warning(f"Could not load metadata: {str(e)}")
        else:
            st.warning("System not initialized")
    
    with tab4:
        st.header("Diagnostics")
        st.markdown("System diagnostic information:")
        
        if 'diagnostics' in st.session_state and st.session_state.diagnostics:
            for i, diagnostic in enumerate(st.session_state.diagnostics[-50:]):  # Show last 50 diagnostics
                st.text(f"{i+1}. {diagnostic}")
        else:
            st.info("No diagnostic information available yet.")
        
        if st.button("Clear Diagnostics"):
            st.session_state.diagnostics = []
            st.rerun()  # Fixed: Updated from st.experimental_rerun()
    
    with tab5:
        st.header("About This System")
        st.markdown("""
        ### Multimodal RAG System
        
        This is an offline Retrieval-Augmented Generation system that can process multiple types of content:
        
        - **Text Documents** (TXT, DOCX, PDF)
        - **Images** (PNG, JPG, JPEG)
        - **Audio** (MP3, WAV)
        
        ### Key Features
        
        1. **Multimodal Processing**: Handles different types of input files
        2. **Semantic Search**: Uses embeddings for intelligent retrieval
        3. **Local LLM**: Uses Microsoft's Phi-3 Mini for answer generation
        4. **Offline Operation**: No internet required after initial setup
        5. **Citation Support**: Provides sources for all retrieved information
        
        ### Technology Stack
        
        - **Text Embedding**: sentence-transformers
        - **Image Embedding**: OpenAI CLIP
        - **Audio Processing**: OpenAI Whisper
        - **Vector Database**: FAISS
        - **LLM**: Microsoft Phi-3 Mini
        - **Framework**: Streamlit
        
        ### How It Works
        
        1. **Ingest**: Documents are processed and converted to embeddings
        2. **Index**: Embeddings are stored in a vector database
        3. **Retrieve**: Queries find similar embeddings in the database
        4. **Generate**: An LLM generates answers based on retrieved context
        
        ### Usage Tips
        
        - Upload documents in the **Ingest** tab
        - Ask questions in the **Chat** tab
        - Check system status in the **Status** tab
        """)
        
        st.markdown("### System Information")
        st.text(f"Python Version: {sys.version}")
        st.text(f"Working Directory: {os.getcwd()}")
        
        # Show LLM status
        if 'initialized' in st.session_state and st.session_state.initialized and st.session_state.generator.model is not None:
            st.success("✅ LLM Model: Loaded successfully")
            if hasattr(st.session_state.generator, 'device'):
                st.text(f"Device: {st.session_state.generator.device}")
                if 'cuda' in str(st.session_state.generator.device):
                    try:
                        import torch
                        gpu_name = torch.cuda.get_device_name(0)
                        st.text(f"GPU: {gpu_name}")
                    except:
                        pass
        else:
            st.warning("⚠️ LLM Model: Not available (using fallback mode)")

if __name__ == "__main__":
    main()