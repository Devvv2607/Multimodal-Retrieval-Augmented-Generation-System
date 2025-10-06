# Streamlit Cloud Deployment Guide

This guide provides step-by-step instructions for deploying the Multimodal RAG System on Streamlit Cloud.

## Prerequisites

1. A GitHub account
2. A Streamlit Cloud account (free at https://streamlit.io/cloud)

## Deployment Steps

### 1. Fork the Repository

1. Go to the GitHub repository page
2. Click the "Fork" button in the top-right corner
3. Choose your GitHub account as the destination for the fork

### 2. Create a New Streamlit App

1. Go to https://streamlit.io/cloud and sign in
2. Click "New app" in the upper right corner
3. Under "Repository", select your forked repository
4. Under "Branch", leave as "main" (or select the branch you want to deploy)
5. Under "Main file path", enter `streamlit_app.py`
6. Under "App URL", choose a memorable name for your app
7. Click "Deploy!"

### 3. Configure Requirements

Streamlit Cloud will automatically detect and install requirements from `requirements.txt`. However, due to system limitations, some dependencies may need special handling:

#### Option 1: Use the Streamlit-specific requirements file

If you encounter issues with the default requirements, you can modify your app settings to use `requirements_streamlit.txt`:

1. In the Streamlit Cloud app settings, look for "Requirements file"
2. Change it from `requirements.txt` to `requirements_streamlit.txt`

#### Option 2: Manual requirements configuration

If needed, you can manually specify requirements in the Streamlit Cloud interface:

```
transformers>=4.35.0
torch>=2.0.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
numpy>=1.21.0
pillow>=9.0.0
python-docx>=0.8.11
pypdf2>=3.0.0
openai-whisper>=20231106
ftfy
regex
tqdm>=4.65.0
pyyaml>=6.0
streamlit>=1.28.0
```

### 4. Handle Optional Dependencies

Due to Streamlit Cloud limitations, some optional dependencies may not install correctly:

#### CLIP (Image Processing)
- CLIP installation from GitHub may fail on Streamlit Cloud
- If this happens, image processing features will be gracefully disabled
- The system will show a warning but continue to function with text and audio processing

#### Whisper (Audio Processing)
- Whisper may not install correctly due to memory or time constraints
- If this happens, audio processing features will be gracefully disabled
- The system will show a warning but continue to function with text and image processing

### 5. Environment Variables

You can set environment variables in the Streamlit Cloud app settings:

1. In your app's settings, find the "Secrets" section
2. Add any needed environment variables:

```
MODEL_CACHE_DIR=/tmp/models
```

## Troubleshooting Common Issues

### 1. Build Timeouts

Streamlit Cloud has a build timeout. If your app fails to build due to timeout:

1. Simplify your requirements.txt to include only essential packages
2. Remove or comment out packages that take a long time to install
3. Consider using pre-built wheels instead of packages that require compilation

### 2. Memory Issues

Streamlit Cloud has memory limitations. If you encounter memory issues:

1. The system is already configured to use CPU-only mode to reduce memory usage
2. Consider using smaller models by modifying config.yaml
3. Process fewer files at a time

### 3. Import Errors

If you see import errors after deployment:

1. Check that all required packages are listed in your requirements file
2. Ensure package versions are compatible
3. Some packages may need to be installed from specific sources (like CLIP from GitHub)

### 4. Model Download Issues

The first time your app runs, it will download models which can take some time:

1. Initial deployment may take several minutes
2. Subsequent runs will be faster as models are cached
3. If models fail to download, check your internet connectivity and try again

## Customizing for Streamlit Cloud

### 1. Configuration

You can customize the application behavior by modifying `config.yaml`:

```yaml
# Reduce model sizes for better performance on Streamlit Cloud
models:
  text_embedding:
    name: "all-MiniLM-L6-v2"  # Smaller, faster model
    dim: 384
  
  llm:
    name: "microsoft/phi-3-mini-4k-instruct"  # Lightweight LLM
    max_tokens: 1024  # Reduce max tokens to save memory
    use_gpu: false  # Always use CPU on Streamlit Cloud

performance:
  use_gpu: false  # Always use CPU
  batch_size: 16  # Reduce batch size to save memory
```

### 2. File Handling

Streamlit Cloud has limitations on file system access:

1. Use relative paths for all file operations
2. Store temporary files in `/tmp` directory
3. Be careful with large file uploads (there are size limits)

## Monitoring and Maintenance

### 1. App Status

Monitor your app's status in the Streamlit Cloud dashboard:

1. Check build logs for any errors
2. Monitor app performance and resource usage
3. View error logs if the app crashes

### 2. Updates

To update your deployed app:

1. Push changes to your GitHub repository
2. Streamlit Cloud will automatically redeploy
3. Or manually trigger a rebuild from the dashboard

### 3. Scaling

Streamlit Cloud automatically scales based on usage:

1. The app will handle multiple concurrent users
2. Very high traffic may require a paid plan
3. Consider caching strategies for better performance

## Best Practices

### 1. Resource Management

1. The system is already configured to use CPU-only mode to avoid GPU-related issues
2. Models are cached after first download
3. Use smaller models when possible

### 2. User Experience

1. Provide clear instructions to users about file size limits
2. Add loading indicators for long-running operations
3. Handle errors gracefully with informative messages

### 3. Security

1. The application processes files locally and doesn't transmit data externally
2. File uploads are processed in temporary directories
3. No authentication is implemented by default

## Support

If you encounter issues with your Streamlit Cloud deployment:

1. Check the build logs for specific error messages
2. Verify all requirements are correctly specified
3. Ensure your repository structure matches the expected format
4. Consult the Streamlit Cloud documentation for platform-specific issues

For issues specific to the Multimodal RAG System:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review the application logs for error messages
3. Ensure system requirements are met