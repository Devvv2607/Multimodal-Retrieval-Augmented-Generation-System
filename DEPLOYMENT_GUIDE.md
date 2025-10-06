# Deployment Guide for Multimodal RAG System

This guide provides detailed instructions for deploying the Multimodal RAG System in various environments.

## Table of Contents
1. [Local Deployment](#local-deployment)
2. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Production Server Deployment](#production-server-deployment)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

## Local Deployment

### Prerequisites
- Python 3.8 or higher
- At least 8GB RAM (16GB recommended)
- Internet connection for initial model downloads

### Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Multimodal-Retrieval-Augmented-Generation-System
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv rag_env
   source rag_env/bin/activate  # On Windows: rag_env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install git+https://github.com/openai/CLIP.git
   pip install streamlit
   ```

4. **Initialize the system**:
   ```bash
   python init.py
   ```

5. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```
   
   Or use the provided scripts:
   - Windows: `run_streamlit.bat`
   - Unix: `run_streamlit.sh`

## Streamlit Cloud Deployment

### Steps

1. **Fork the repository** to your GitHub account

2. **Create a new app** on [Streamlit Cloud](https://streamlit.io/cloud):
   - Connect it to your forked repository
   - Set the main file path to `streamlit_app.py`

3. **Configure requirements**:
   Due to Streamlit Cloud limitations, some dependencies may need special handling:
   - The system will automatically use `requirements_streamlit.txt`
   - CLIP installation may be skipped (image processing will be limited)
   - Whisper installation may be skipped (audio processing will be disabled)

4. **Set environment variables** (if needed):
   - `MODEL_CACHE_DIR`: Directory for caching models

### Handling Dependencies on Streamlit Cloud

Some dependencies may not install correctly on Streamlit Cloud due to system limitations:

1. For CLIP installation issues, the system will gracefully degrade with limited image processing capabilities.

2. If Whisper is not available, audio processing will be disabled.

3. You can use the simplified requirements file:
   ```bash
   pip install -r requirements_streamlit.txt
   ```

## Docker Deployment

### Building the Docker Image

1. **Create a Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Install CLIP
   RUN pip install git+https://github.com/openai/CLIP.git
   
   # Install Streamlit
   RUN pip install streamlit
   
   COPY . .
   
   # Initialize the system
   RUN python init.py
   
   EXPOSE 8501
   
   HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
   
   ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build the image**:
   ```bash
   docker build -t multimodal-rag .
   ```

3. **Run the container**:
   ```bash
   docker run -p 8501:8501 multimodal-rag
   ```

### Docker Compose (Optional)

Create a `docker-compose.yml` file:
```yaml
version: '3.8'
services:
  rag-app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - MODEL_CACHE_DIR=/app/models/cache
```

Run with:
```bash
docker-compose up
```

## Production Server Deployment

### Using Gunicorn and Nginx

1. **Install additional dependencies**:
   ```bash
   pip install gunicorn
   ```

2. **Create a Streamlit wrapper** (`app.py`):
   ```python
   import streamlit.web.bootstrap
   import os
   
   if __name__ == '__main__':
       os.environ["STREAMLIT_SERVER_PORT"] = "8501"
       os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
       streamlit.web.bootstrap.run("streamlit_app.py", '', [], {})
   ```

3. **Create a Gunicorn configuration** (`gunicorn.conf.py`):
   ```python
   bind = "0.0.0.0:8501"
   workers = 1
   threads = 4
   timeout = 120
   ```

4. **Run with Gunicorn**:
   ```bash
   gunicorn -c gunicorn.conf.py app:app
   ```

5. **Configure Nginx** as a reverse proxy:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Environment Variables

The following environment variables can be set to customize the deployment:

- `MODEL_CACHE_DIR`: Directory for caching models (default: `./models/cache`)
- `STREAMLIT_SERVER_PORT`: Port for Streamlit server (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Address for Streamlit server (default: localhost)

## Troubleshooting

### Common Issues

1. **LLM Loading Error**: If you see "requires accelerate" error, install it with:
   ```bash
   pip install accelerate
   ```

2. **Port Conflicts**: If port 8501 is in use, Streamlit will automatically use another port

3. **Model Download Issues**: Ensure internet connectivity for initial model downloads

4. **Memory Issues**: For systems with limited RAM, consider:
   - Using smaller models
   - Processing files in smaller batches
   - Increasing virtual memory/swap space

5. **GPU Issues**: If experiencing GPU-related errors:
   - The system is configured to use CPU by default to avoid device-related errors
   - Ensure proper CUDA installation if you want to use GPU

### Deployment Scripts

The project includes deployment helper scripts:

- `setup_deploy.py`: Automated setup script for different deployment environments
- `deploy.py`: Simplified deployment application with graceful degradation
- `verify_deploy.py`: Script to verify deployment setup

To run the setup script:
```bash
python setup_deploy.py
```

For Streamlit Cloud deployment:
```bash
python setup_deploy.py --streamlit-cloud
```

## Performance Tips

1. **Hardware Requirements**:
   - Minimum: 8GB RAM, modern CPU
   - Recommended: 16GB+ RAM, CUDA-compatible GPU

2. **Optimization**:
   - Process files in batches for better efficiency
   - Use smaller models if running on limited hardware
   - Monitor system resources during heavy processing
   - Clear chat history periodically to reduce memory usage

3. **Model Caching**:
   - Models are cached after first download
   - Set `MODEL_CACHE_DIR` to a persistent volume in containerized deployments

## Security Considerations

1. **Data Privacy**:
   - The application runs locally and does not transmit data externally
   - File uploads are processed in temporary directories

2. **Authentication**:
   - No authentication is implemented by default
   - For production use, consider adding authentication and access controls

3. **Network Security**:
   - When deploying to production, use HTTPS
   - Restrict access to authorized users only
   - Regularly update dependencies to patch security vulnerabilities

## Support

For issues with deployment, please:
1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review the logs for error messages
3. Ensure all dependencies are correctly installed
4. Verify system requirements are met