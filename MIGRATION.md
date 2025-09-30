# Migration from Streamlit to Flask

This document provides information about the conversion from Streamlit to Flask.

## What Changed?

The application has been completely rewritten to use Flask instead of Streamlit, while maintaining all the same functionality.

### Key Differences

| Feature | Streamlit (Old) | Flask (New) |
|---------|----------------|-------------|
| **Framework** | Streamlit | Flask |
| **Port** | 8501 | 5000 |
| **Start Command** | `streamlit run app.py` | `python app.py` or `flask run` |
| **API Key Config** | `.streamlit/secrets.toml` or sidebar | Environment variable or web form |
| **UI** | Streamlit widgets | Custom HTML/CSS templates |
| **State Management** | Streamlit session state | Flask sessions |

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
Choose one of these methods to set your API key:

**Option 1: Environment Variable (Recommended for production)**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Option 2: .env File**
```bash
cp .env.example .env
# Edit .env and add your API key
```

**Option 3: Web Form (Good for testing)**
Just enter your API key in the web interface when prompted.

### Running the Application
```bash
python app.py
```
Then open your browser to http://localhost:5000

## What Stayed the Same?

- ✅ All document processing functionality (PDF, DOCX, TXT, HTML)
- ✅ Default template support
- ✅ Custom template uploads
- ✅ Google Gemini AI integration
- ✅ DOCX download capability
- ✅ Same workflow: upload template and lease, generate term sheet, download

## Security Improvements

The Flask version includes several security enhancements:

1. **Path Injection Prevention**: File paths are never exposed to user input
2. **Debug Mode Disabled**: Debug mode is off by default in production
3. **Secure File Uploads**: Using Werkzeug's secure filename validation
4. **File Size Limits**: 16MB maximum upload size
5. **Session Security**: API keys stored in secure sessions, never on disk

## Why Flask?

Flask offers several advantages:
- More control over the UI/UX
- Better suited for production deployments
- Easier to integrate with existing web infrastructure
- More flexible routing and API design
- Standard web development patterns

## Need Help?

- Check the [README.md](README.md) for detailed installation and usage instructions
- Review [SETUP_API_KEY.md](SETUP_API_KEY.md) for API key configuration options
- The original Streamlit version is preserved as `app_streamlit.py` for reference

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
flask run --port 8080
```

### API Key Not Working
Make sure you've set the environment variable or entered it in the web form.

### File Upload Issues
Ensure files are under 16MB and in supported formats (PDF, DOCX, TXT, HTML).
