# Streamlit Cloud Deployment Troubleshooting

This guide helps troubleshoot common issues when deploying the Multimodal RAG System on Streamlit Cloud.

## Common Error: "Error running app"

This is the most common error message you might see on Streamlit Cloud. Here are the steps to resolve it:

### 1. Check Build Logs

First, check the build logs in Streamlit Cloud:

1. Go to your app dashboard
2. Click on the "Logs" tab
3. Look for specific error messages during the build process

### 2. Verify Requirements File

The most common cause of deployment errors is incorrect or missing requirements:

#### Option A: Use Minimal Requirements
Try using the minimal requirements file:
```
# In your Streamlit Cloud app settings, set requirements file to:
requirements_minimal.txt
```

#### Option B: Check Your Current Requirements
Verify that your requirements file includes all necessary packages:
```
transformers>=4.35.0
torch>=2.0.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
numpy>=1.21.0
pillow>=9.0.0
python-docx>=0.8.11
pypdf2>=3.0.0
pyyaml>=6.0
streamlit>=1.28.0
```

### 3. Check File Structure

Ensure your repository has the correct structure:

```
your-repo/
├── streamlit_app.py     # Main file (must be in root)
├── config.yaml          # Configuration file
├── requirements.txt     # Requirements file
└── ... (other files and directories)
```

### 4. Verify Main File Path

In your Streamlit Cloud app settings:
- Main file path should be: `streamlit_app.py`
- Not: `src/streamlit_app.py` or any other path

## Dependency Issues

### CLIP Installation Problems

CLIP often fails to install on Streamlit Cloud due to compilation requirements:

1. Remove CLIP from your requirements file:
   ```
   # Remove this line if present:
   # git+https://github.com/openai/CLIP.git
   ```

2. The system will gracefully degrade without image processing capabilities

### Whisper Installation Problems

Whisper may fail due to memory or time constraints:

1. Remove Whisper from your requirements file:
   ```
   # Remove this line if present:
   # openai-whisper>=20231106
   ```

2. The system will gracefully degrade without audio processing capabilities

## Memory Issues

Streamlit Cloud has memory limitations that can cause apps to crash:

### Solutions:

1. **Use CPU-only mode** (already configured):
   - The system is already configured to use CPU to avoid GPU memory issues

2. **Reduce model sizes** in `config.yaml`:
   ```yaml
   models:
     text_embedding:
       name: "all-MiniLM-L6-v2"  # Smaller model
       dim: 384
   
     llm:
       name: "microsoft/phi-3-mini-4k-instruct"  # Lightweight LLM
       max_tokens: 1024  # Reduce max tokens
   ```

3. **Process smaller files**:
   - Encourage users to upload smaller files
   - Implement file size checks in the app

## Timeout Issues

Streamlit Cloud has build timeouts that can cause deployment failures:

### Solutions:

1. **Use pre-built packages**:
   - Avoid packages that require compilation
   - Use packages from PyPI when possible

2. **Simplify requirements**:
   - Remove non-essential packages
   - Use minimal requirements for initial deployment

3. **Initial model download**:
   - First deployment may take longer due to model downloads
   - Subsequent deployments will be faster due to caching

## Import Errors

### "Module not found" errors:

1. **Check package names**:
   - Ensure package names in requirements match import statements
   - Some packages have different import names than their PyPI names

2. **Check package versions**:
   - Ensure version requirements are compatible
   - Try using more permissive version requirements

3. **Verify dependencies**:
   - Some packages require specific versions of other packages
   - Check for version conflicts

## Configuration Issues

### Missing config.yaml:

1. **Verify file exists**:
   - Ensure `config.yaml` is in the root directory
   - Check file name spelling and case

2. **Check file format**:
   - Ensure proper YAML formatting
   - Use a YAML validator to check syntax

### Path Issues:

1. **Use relative paths**:
   - All paths in `config.yaml` should be relative
   - Avoid absolute paths

2. **Check directory structure**:
   - Ensure referenced directories exist
   - Create directories if needed

## Testing Your Fix

### 1. Local Testing:

Before redeploying, test locally:

```bash
# Create a new virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install minimal requirements
pip install -r requirements_minimal.txt

# Test the app
streamlit run streamlit_app.py
```

### 2. GitHub Update:

1. Push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Fix Streamlit Cloud deployment issues"
   git push
   ```

2. Streamlit Cloud will automatically redeploy

### 3. Manual Redeploy:

If automatic redeployment doesn't work:
1. Go to your app dashboard
2. Click "Reboot app" or "Delete and recreate"

## Alternative Deployment

If you continue to have issues:

### Option 1: Use the Simplified App

Deploy the simplified version:

1. In Streamlit Cloud settings, change the main file path to:
   ```
   streamlit_cloud_app.py
   ```

### Option 2: Use Minimal Requirements

1. In Streamlit Cloud settings, set requirements file to:
   ```
   requirements_minimal.txt
   ```

## Getting Help

If you're still experiencing issues:

1. **Check Streamlit Community**:
   - https://discuss.streamlit.io/

2. **Review Streamlit Cloud Documentation**:
   - https://docs.streamlit.io/cloud

3. **Share Specific Error Messages**:
   - Include the exact error from the build logs
   - Share your requirements file
   - Mention which deployment option you're using

## Prevention

To avoid future deployment issues:

1. **Test locally first**:
   - Always test changes locally before deploying

2. **Incremental changes**:
   - Make small changes and test frequently

3. **Version control**:
   - Keep working versions in separate branches

4. **Documentation**:
   - Keep notes of what works and what doesn't