# Multimodal RAG System - Project Structure

## Overview
This document provides a detailed overview of the project structure for the Multimodal Retrieval-Augmented Generation (RAG) system.

## Directory Structure
```
multimodal_rag/
├── embedding/                 # Embedding generation modules
│   ├── audio_embedder.py      # Audio transcription and embedding
│   ├── image_embedder.py      # Image embedding using CLIP
│   └── text_embedder.py       # Text embedding using sentence transformers
├── generation/                # LLM-based answer generation
│   └── generator.py           # Phi-3 Mini integration and prompt engineering
├── indexing/                  # Vector database management
│   └── vector_store.py        # FAISS vector store implementation
├── ingestion/                 # File processing and content extraction
│   ├── audio_processor.py     # Audio file processing
│   ├── document_processor.py  # DOCX/PDF text extraction
│   ├── image_processor.py     # Image file processing
│   ├── ingestor.py            # Main ingestion coordinator
│   └── text_processor.py      # Plain text processing
├── models/                    # Model management
│   └── setup_models.py        # Model downloading and setup
├── query/                     # User interfaces
│   ├── cli_interface.py       # Command-line interface
│   └── gui_interface.py       # Graphical user interface
├── retrieval/                 # Content retrieval logic
│   └── retriever.py           # Multimodal retrieval implementation
├── utils/                     # Utility functions
│   ├── config.py              # Configuration management
│   └── logger.py              # Logging utilities
├── config.yaml                # System configuration
├── example_usage.py           # Example usage demonstration
├── init.py                    # System initialization
├── main.py                    # Main entry point
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
├── setup_env.bat              # Windows environment setup
├── setup_env.sh               # Unix environment setup
└── test_system.py             # System testing
```

## Component Descriptions

### Ingestion Layer
Handles processing of different file types:
- **document_processor.py**: Extracts text from DOCX and PDF files
- **image_processor.py**: Processes image files for metadata
- **audio_processor.py**: Handles audio file processing
- **text_processor.py**: Processes plain text files with chunking
- **ingestor.py**: Coordinates the entire ingestion process

### Embedding Layer
Generates vector representations for different modalities:
- **text_embedder.py**: Uses sentence-transformers for text embeddings
- **image_embedder.py**: Uses OpenAI CLIP for image embeddings
- **audio_embedder.py**: Uses Whisper for speech transcription and text embedding

### Indexing Layer
Manages the vector database:
- **vector_store.py**: FAISS-based vector storage with metadata management

### Retrieval Layer
Performs similarity search across all modalities:
- **retriever.py**: Implements text-to-text, text-to-image, and image-to-text retrieval

### Generation Layer
Uses local LLM for answer generation:
- **generator.py**: Integrates Microsoft's Phi-3 Mini with prompt engineering

### Query Interface
Provides user interaction:
- **cli_interface.py**: Command-line interface for scripting
- **gui_interface.py**: Graphical interface for interactive use

### Utilities
Supporting functionality:
- **config.py**: YAML-based configuration management
- **logger.py**: Logging with both console and file output

## Key Features Implemented

1. **Multimodal Input Processing**: Supports DOCX, PDF, images, and audio files
2. **Unified Vector Database**: Stores embeddings from all modalities in FAISS
3. **Cross-Modal Retrieval**: Text-to-text, text-to-image, image-to-text, audio-to-text
4. **Local LLM Integration**: Uses Microsoft's Phi-3 Mini for answer generation
5. **Citation Support**: Provides source references for all retrieved content
6. **Offline Operation**: No external API calls required
7. **Modular Architecture**: Clean separation of concerns
8. **Multiple Interfaces**: Both CLI and GUI options
9. **Comprehensive Logging**: Detailed logging for debugging and monitoring
10. **Configuration Management**: Flexible YAML-based configuration

## Usage Examples

### Command Line Interface
```bash
# Process documents
python main.py ingest --input_dir /path/to/documents

# Query the system
python main.py query --question "Your question here"

# Launch GUI
python main.py --gui
```

### Programmatic Usage
```python
from ingestion.ingestor import Ingestor
from retrieval.retriever import Retriever
from generation.generator import Generator

# Initialize components
ingestor = Ingestor()
ingestor.ingest_directory("/path/to/documents")

# Query
retriever = Retriever(vector_store, text_embedder, image_embedder)
context = retriever.retrieve_text("Your question")

# Generate answer
generator = Generator()
answer = generator.generate_answer("Your question", context)
```

## System Requirements
- Python 3.8 or higher
- At least 8GB RAM (16GB recommended)
- CUDA-compatible GPU recommended but not required
- Approximately 10GB disk space for models and data

## Model Requirements
- **Text Embedding**: sentence-transformers/all-MiniLM-L6-v2
- **Image Embedding**: OpenAI CLIP ViT-B/32
- **Audio Processing**: OpenAI Whisper base model
- **LLM**: Microsoft Phi-3 Mini 4K Instruct

## Configuration
The system is configured through `config.yaml` which allows customization of:
- Model paths and parameters
- Vector database settings
- Processing parameters
- Retrieval settings