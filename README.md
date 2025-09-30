# Lease Term Sheet Generator

A Streamlit application that automatically generates lease term sheets by analyzing commercial lease documents and matching them to your template format using Google Gemini AI.

## Features

- 📄 Upload lease term sheet templates (PDF, DOCX, or TXT)
- 📑 Upload commercial lease documents (PDF, DOCX, or TXT)
- 🤖 AI-powered analysis using Google Gemini
- 🔑 Optional default API key configuration
- 📋 Generates term sheets matching your template format
- ⬇️ Download generated term sheets
- 🎨 Clean, user-friendly interface

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

3. (Optional) Configure a default API key:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Then edit `.streamlit/secrets.toml` and add your Gemini API key. See [SETUP_API_KEY.md](SETUP_API_KEY.md) for details.

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

3. If you haven't configured a default API key:
   - Enter your Google Gemini API key in the sidebar

4. Upload your lease term sheet template

5. Upload the commercial lease document you want to analyze

6. Click "Generate Term Sheet" to create your term sheet

7. Download the generated term sheet using the download button

## How It Works

1. **Document Reading**: The app reads both your template and lease documents, supporting PDF, DOCX, and TXT formats
2. **AI Analysis**: Using Google Gemini, the app analyzes the commercial lease to extract key information
3. **Term Sheet Generation**: The AI generates a term sheet that matches your template's structure and format
4. **Download**: Export the generated term sheet for your use

## Supported File Formats

- PDF (.pdf)
- Microsoft Word (.docx)
- Plain Text (.txt)

## Security Note

If you configure a default API key, it's stored in `.streamlit/secrets.toml` which is excluded from version control. You can also enter an API key directly in the app sidebar - it's only stored in your browser session and is never saved to disk. Always keep your API key secure and never share it publicly.

## Dependencies

- `streamlit`: Web application framework
- `PyPDF2`: PDF document reading
- `python-docx`: DOCX document reading
- `google-generativeai`: Google Gemini API integration

## Troubleshooting

### Gemini API Model Errors

If you encounter errors related to Gemini models, see [GEMINI_MODELS.md](GEMINI_MODELS.md) for:
- List of supported models
- Common error solutions
- API key requirements

## License

This project is open source and available for use.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.