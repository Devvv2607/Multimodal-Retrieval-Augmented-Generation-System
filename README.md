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

## Deployment

### Automated Deployment Scripts

The project now includes several automated deployment scripts:

- `deploy_app.py`: Python script for various deployment options
- `deploy.sh`: Bash script for Unix-like systems
- `deploy.bat`: Batch script for Windows systems
- `DEPLOYMENT_GUIDE.md`: Comprehensive deployment guide

To use the Python deployment script:
```bash
python deploy_app.py --local [--run]
```

To use the bash script (Unix/Linux/Mac):
```bash
./deploy.sh
```

To use the batch script (Windows):
```bash
deploy.bat
```

### Streamlit Cloud Deployment

To deploy on Streamlit Cloud:

1. Fork this repository to your GitHub account
2. Create a new app on Streamlit Cloud
3. Connect it to your forked repository
4. Set the main file path to `streamlit_app.py`

For detailed Streamlit Cloud deployment instructions, see:
- [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md) - Complete guide
- [requirements_streamlit_cloud.txt](requirements_streamlit_cloud.txt) - Optimized requirements for Streamlit Cloud
- [STREAMLIT_CLOUD_TROUBLESHOOTING.md](STREAMLIT_CLOUD_TROUBLESHOOTING.md) - Troubleshooting guide for deployment issues

### Handling Dependencies on Streamlit Cloud

Some dependencies may not install correctly on Streamlit Cloud due to system limitations:

1. For CLIP installation issues, you can use the simplified requirements file:
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. If CLIP is not available, the system will gracefully degrade with limited image processing capabilities.

3. If Whisper is not available, audio processing will be disabled.

### Docker Deployment

To deploy using Docker:

1. Build the Docker image:
   ```bash
   docker build -t multimodal-rag .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 multimodal-rag
   ```

### Environment Variables

Set the following environment variables if needed:
- `MODEL_CACHE_DIR`: Directory for caching models (default: `./models/cache`)

### Deployment Scripts

The project includes deployment helper scripts:

- `setup_deploy.py`: Automated setup script for different deployment environments
- `deploy.py`: Simplified deployment application with graceful degradation
- `setup_streamlit.py`: Streamlit Cloud specific setup script
- `test_minimal.py`: Minimal test to verify deployment setup

To run the setup script:
```bash
python setup_deploy.py
```

For Streamlit Cloud deployment:
```bash
python setup_deploy.py --streamlit-cloud
```

## Troubleshooting

If you encounter issues with deployment:

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for general issues
2. For Streamlit Cloud specific issues, see [STREAMLIT_CLOUD_TROUBLESHOOTING.md](STREAMLIT_CLOUD_TROUBLESHOOTING.md)
3. Run the diagnostic script: `python comprehensive_diagnostic.py`

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