# Multimodal RAG System - Streamlit Application

## Overview
The Streamlit application provides a user-friendly web interface for the Multimodal RAG System, allowing users to easily ingest documents, ask questions, and view system status through a modern web UI.

## Features
- **Document Ingestion**: Upload and process multiple file types
- **Chat Interface**: Interactive question-answering with chat history
- **System Status**: Real-time monitoring of indexed content
- **Responsive Design**: Works on desktop and mobile devices
- **Offline Operation**: No internet required after initial setup

## File Structure
```
streamlit_app.py        # Main Streamlit application
run_streamlit.bat       # Windows launcher script
run_streamlit.sh        # Unix launcher script
test_streamlit.py       # Import verification script
```

## Installation
The Streamlit application requires the base RAG system to be set up first:

```bash
# Activate virtual environment
source rag_env/bin/activate  # On Windows: rag_env\Scripts\activate

# Install Streamlit
pip install streamlit

# Install accelerate for LLM support
pip install accelerate
```

## Usage
1. **Launch the Application**:
   ```bash
   streamlit run streamlit_app.py
   ```
   
   Or use the provided launcher scripts:
   - Windows: `run_streamlit.bat`
   - Unix: `run_streamlit.sh`

2. **Access the Web Interface**:
   Open your browser and navigate to http://localhost:8501

## Application Tabs

### 1. Ingest Tab
- Upload multiple files (TXT, DOCX, PDF, PNG, JPG, MP3, WAV)
- Process files with a single click
- View supported file types and system feedback

### 2. Chat Tab
- Interactive chat interface with conversation history
- Ask questions about indexed content
- View answers with source citations
- Real-time processing feedback

### 3. Status Tab
- View system metrics (indexed vectors count)
- Check configuration settings
- See indexed content summary
- View metadata of processed files

### 4. About Tab
- System documentation and usage tips
- Technology stack overview
- How the system works
- System information

## Supported File Types
- **Text Documents**: .txt
- **Word Documents**: .docx
- **PDF Documents**: .pdf
- **Images**: .png, .jpg, .jpeg
- **Audio**: .mp3, .wav

## System Requirements
- Python 3.8 or higher
- At least 8GB RAM (16GB recommended)
- CUDA-compatible GPU recommended but not required

## Troubleshooting
1. **LLM Loading Error**: If you see "requires accelerate" error, install it with:
   ```bash
   pip install accelerate
   ```

2. **Port Conflicts**: If port 8501 is in use, Streamlit will automatically use another port

3. **Model Download Issues**: Ensure internet connectivity for initial model downloads

## Customization
The Streamlit app can be customized by modifying `streamlit_app.py`:
- Change page title and layout in `st.set_page_config()`
- Modify UI elements and styling
- Add new tabs or functionality
- Adjust processing parameters

## API Integration
The Streamlit app uses the same backend components as the CLI and GUI:
- Ingestor for file processing
- Retriever for content search
- Generator for answer creation
- VectorStore for data management

## Security Considerations
- The application runs locally and does not transmit data externally
- File uploads are processed in temporary directories
- No authentication is implemented by default
- For production use, consider adding authentication and access controls

## Performance Tips
- Process files in batches for better efficiency
- Use smaller models if running on limited hardware
- Monitor system resources during heavy processing
- Clear chat history periodically to reduce memory usage