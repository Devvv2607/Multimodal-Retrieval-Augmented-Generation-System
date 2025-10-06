# Multimodal Retrieval-Augmented Generation (RAG) System

An offline multimodal RAG system that processes documents, images, and audio to provide intelligent search and question answering capabilities.

## Features

- **Multimodal Input Processing**: Supports DOCX, PDF, images, and audio files
- **Unified Vector Database**: Stores embeddings from all modalities in FAISS
- **Cross-Modal Retrieval**: Text-to-text, text-to-image, image-to-text, audio-to-text
- **Local LLM Integration**: Uses Microsoft's Phi-3 Mini for answer generation
- **Citation Support**: Provides source references for all retrieved content
- **Offline Operation**: No external API calls required

## Project Structure

```
multimodal_rag/
├── ingestion/          # File processing and content extraction
├── embedding/          # Embedding generation for different modalities
├── indexing/           # Vector database management
├── retrieval/          # Content retrieval logic
├── generation/         # LLM-based answer generation
├── query/              # Query interface
├── utils/              # Utility functions
├── models/             # Model management
├── main.py             # Entry point
├── config.yaml         # Configuration file
└── requirements.txt    # Dependencies
```

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv rag_env
   source rag_env/bin/activate  # On Windows: rag_env\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install git+https://github.com/openai/CLIP.git
   pip install streamlit
   ```

3. Initialize the system:
   ```bash
   python init.py
   ```

4. Download required models:
   ```bash
   python models/setup_models.py
   ```

## Usage

### Command Line Interface
1. Process documents:
   ```bash
   python main.py ingest --input_dir /path/to/documents
   ```

2. Query the system:
   ```bash
   python main.py query --question "Your question here"
   ```

### Graphical User Interface
Launch the Tkinter GUI:
```bash
python main.py --gui
```

### Web Interface (Streamlit)
Launch the Streamlit web app:
```bash
streamlit run streamlit_app.py
```

Or use the provided scripts:
- On Windows: `run_streamlit.bat`
- On Unix-like systems: `run_streamlit.sh`

The app will be available at: http://localhost:8501

## System Components

### Ingestion
The ingestion module handles processing of different file types:
- **Documents** (DOCX, PDF): Extracts text content
- **Images**: Processes image files for embedding
- **Audio**: Transcribes speech and processes audio files
- **Text**: Processes plain text files

### Embedding
The embedding module generates vector representations:
- **Text Embedding**: Uses sentence-transformers
- **Image Embedding**: Uses OpenAI CLIP
- **Audio Embedding**: Uses Whisper for transcription, then text embedding

### Indexing
The indexing module stores embeddings in a FAISS vector database with metadata.

### Retrieval
The retrieval module performs similarity search across all modalities.

### Generation
The generation module uses Microsoft's Phi-3 Mini LLM to generate answers based on retrieved context.

## Configuration

Edit `config.yaml` to adjust model paths, embedding dimensions, and other parameters.

## Testing

Run the test suite to verify system functionality:
```bash
python test_system.py
```

## License

This project is licensed under the MIT License.