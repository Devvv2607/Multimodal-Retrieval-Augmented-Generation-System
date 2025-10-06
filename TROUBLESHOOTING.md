# Troubleshooting Guide - Multimodal RAG System

## Common Issues and Solutions

### 1. System Not Answering Questions

#### Symptoms
- Files are processed successfully
- System shows indexed vectors
- But questions return no answers or "I don't know" responses

#### Diagnosis Steps

1. **Check Indexed Content**:
   ```bash
   python main.py status
   ```
   Verify that there are indexed vectors (> 0).

2. **Test Retrieval Directly**:
   Create a test script to verify retrieval is working:
   ```python
   from retrieval.retriever import Retriever
   from indexing.vector_store import VectorStore
   from embedding.text_embedder import TextEmbedder
   from embedding.image_embedder import ImageEmbedder
   from utils.config import config
   
   # Initialize components
   vector_store = VectorStore(
       dimension=config.get('models.text_embedding.dim', 384),
       index_path=config.get('vector_db.index_path'),
       metadata_path=config.get('vector_db.metadata_path')
   )
   
   text_embedder = TextEmbedder(config.get('models.text_embedding.name'))
   image_embedder = ImageEmbedder(config.get('models.image_embedding.name'))
   retriever = Retriever(vector_store, text_embedder, image_embedder)
   
   # Test query
   results = retriever.retrieve_text("your test query", k=3)
   print(f"Retrieved {len(results)} results")
   ```

3. **Check Metadata Content**:
   Look at the metadata.json file to verify content was properly indexed:
   ```bash
   cat data/metadata.json
   ```

#### Solutions

1. **Ensure Content Relevance**:
   - Make sure your questions are related to the content you've ingested
   - Try more general queries if specific ones don't work

2. **Check Embedding Quality**:
   - Verify that text was properly extracted from your documents
   - Check that the text chunks contain meaningful content

3. **Adjust Similarity Threshold**:
   In `config.yaml`, you can adjust the retrieval settings:
   ```yaml
   retrieval:
     top_k: 5
     similarity_threshold: 0.5  # Lower this if needed
   ```

### 2. LLM Not Generating Answers

#### Symptoms
- Retrieval works (shows relevant context)
- But LLM doesn't generate proper answers
- Shows raw context instead of generated responses

#### Diagnosis Steps

1. **Check LLM Status**:
   In the Streamlit app, check the Status tab for LLM status indicator.

2. **Verify Model Loading**:
   ```python
   from generation.generator import Generator
   gen = Generator()
   print("Model loaded:", gen.model is not None)
   ```

#### Solutions

1. **Install Required Dependencies**:
   ```bash
   pip install accelerate
   ```

2. **Check System Resources**:
   - Ensure you have enough RAM (8GB minimum, 16GB recommended)
   - Close other applications to free up memory

3. **Use Smaller Models**:
   Modify `config.yaml` to use smaller models:
   ```yaml
   models:
     llm:
       name: "microsoft/phi-3-mini-4k-instruct"
       max_tokens: 1024  # Reduce if needed
   ```

### 3. Files Not Being Processed

#### Symptoms
- Files are uploaded but not indexed
- Status shows 0 vectors after ingestion

#### Diagnosis Steps

1. **Check File Formats**:
   Ensure files are in supported formats:
   - Text: .txt
   - Documents: .docx, .pdf
   - Images: .png, .jpg, .jpeg
   - Audio: .mp3, .wav

2. **Check File Content**:
   - Ensure files contain actual content (not empty)
   - For PDFs, ensure they contain text (not just images)

#### Solutions

1. **Verify File Processing**:
   Check the logs for any error messages during ingestion.

2. **Test with Simple Files**:
   Try processing simple .txt files first to verify the pipeline works.

### 4. Streamlit App Issues

#### Symptoms
- App doesn't start
- App starts but shows errors
- App is slow or unresponsive

#### Solutions

1. **Restart the App**:
   ```bash
   # Kill existing processes
   taskkill /f /im streamlit.exe
   
   # Restart
   streamlit run streamlit_app.py
   ```

2. **Check Port Conflicts**:
   Streamlit will automatically use another port if 8501 is busy.

3. **Clear Browser Cache**:
   Sometimes browser caching can cause issues.

## Debugging Commands

### Check System Status
```bash
python main.py status
```

### Test Component Imports
```bash
python -c "from ingestion.ingestor import Ingestor; print('Ingestor OK')"
python -c "from retrieval.retriever import Retriever; print('Retriever OK')"
python -c "from generation.generator import Generator; print('Generator OK')"
```

### Check Data Directory
```bash
ls -la data/
```

### Test Query Directly
```bash
python main.py query --question "What is machine learning?"
```

## Configuration Issues

### Vector Database Path Issues
Ensure paths in `config.yaml` are correct:
```yaml
vector_db:
  type: "faiss"
  index_path: "./data/index.faiss"
  metadata_path: "./data/metadata.json"
```

### Model Configuration
Verify model names are correct:
```yaml
models:
  text_embedding:
    name: "all-MiniLM-L6-v2"
    dim: 384
  image_embedding:
    name: "clip"
    dim: 512
  llm:
    name: "microsoft/phi-3-mini-4k-instruct"
    max_tokens: 2048
```

## Performance Optimization

### For Low-Memory Systems
1. Use smaller models
2. Reduce batch sizes
3. Process files one at a time
4. Clear chat history periodically

### For Faster Processing
1. Use SSD storage
2. Ensure adequate RAM
3. Close unnecessary applications
4. Use GPU if available

## Contact Support

If you continue to experience issues:

1. Check all error messages in the console
2. Verify all dependencies are installed
3. Ensure you're using the correct Python environment
4. Check that all file paths are correct

For additional help, please provide:
- Error messages
- System specifications
- Steps to reproduce the issue