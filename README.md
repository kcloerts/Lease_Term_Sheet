# Lease Term Sheet Generator

A Flask web application that automatically generates lease term sheets by analyzing commercial lease documents using Google Gemini AI. A default template is built-in, or you can provide your own custom template.

## Features

- 📋 Built-in default lease term sheet template (`Term Sheet Template_app.html`)
- 📄 Optional custom template upload (PDF, DOCX, TXT, or HTML)
- 📑 Upload commercial lease documents (PDF, DOCX, or TXT)
- 🤖 AI-powered analysis using Google Gemini
- 🔑 Flexible API key configuration (environment variable or web form)
- 📋 Generates term sheets matching the template format
- ⬇️ Download generated term sheets as Word documents (.docx)
- 🎨 Clean, responsive web interface

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key: Get one at [Google AI Studio](https://makersuite.google.com/app/apikey)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/kcloerts/Lease_Term_Sheet.git
cd Lease_Term_Sheet
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Configure a default API key as an environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root:
```
GEMINI_API_KEY=your-api-key-here
SECRET_KEY=your-secret-key-here
```

## Usage

1. Start the Flask app:
```bash
python app.py
```

Or use the Flask CLI:
```bash
flask run
```

2. Open your browser and navigate to `http://localhost:5000`

3. **Configure API Key**:
   - Option 1: Set the `GEMINI_API_KEY` environment variable (recommended for production)
   - Option 2: Enter your API key directly in the web interface (stored in session only)

4. **Template Options**:
   - By default, the app uses the built-in `Term Sheet Template_app.html` template
   - To use a custom template: Check "Use custom template" and upload your template file
   - To view the default template: Click the "View Default Template" dropdown

5. Upload the commercial lease document you want to analyze

6. Click "Generate Term Sheet" to create your term sheet

7. Download the generated term sheet using the download button

## How It Works

1. **Template Selection**: The app uses the built-in default template (`Term Sheet Template_app.html`) or accepts a custom template (PDF, DOCX, TXT, or HTML)
2. **Document Reading**: The app reads your lease document, supporting PDF, DOCX, and TXT formats
3. **AI Analysis**: Using Google Gemini, the app analyzes the commercial lease to extract key information
4. **Term Sheet Generation**: The AI generates a term sheet that matches the template's structure and format
5. **Download**: Export the generated term sheet as a Word document (.docx) for easy editing and sharing

## Supported File Formats

**For Lease Documents:**
- PDF (.pdf)
- Microsoft Word (.docx)
- Plain Text (.txt)

**For Templates:**
- PDF (.pdf)
- Microsoft Word (.docx)
- Plain Text (.txt)
- HTML (.htm, .html)

## Security Note

API keys can be configured in two ways:
1. **Environment Variable** (recommended): Set `GEMINI_API_KEY` in your environment or `.env` file
2. **Web Form**: Enter directly in the application - stored only in the session (not saved to disk)

Always keep your API key secure and never commit it to version control. The `.env` file is excluded from git via `.gitignore`.

## Dependencies

- `Flask`: Web application framework
- `PyPDF2`: PDF document reading
- `python-docx`: DOCX document reading and writing
- `google-generativeai`: Google Gemini API integration

## Troubleshooting

### Gemini API Model Errors

If you encounter errors related to Gemini models, see [GEMINI_MODELS.md](GEMINI_MODELS.md) for:
- List of supported models
- Common error solutions
- API key requirements

### Port Already in Use

If port 5000 is already in use, you can specify a different port:
```bash
flask run --port 8080
```

## License

This project is open source and available for use.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.