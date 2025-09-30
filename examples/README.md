# Example Documents

This folder contains sample documents you can use to test the Lease Term Sheet Generator application.

## Files

- **sample_template.txt**: A sample lease term sheet template with placeholders
- **sample_lease.txt**: A sample commercial lease agreement with complete details

## How to Use

1. Start the application: `python app.py` or `flask run`
2. Open your browser to `http://localhost:5000`
3. Configure your Google Gemini API key (via environment variable or web form)
4. Check "Use custom template" and upload `sample_template.txt` as your template (or use the default)
5. Upload `sample_lease.txt` as your commercial lease
6. Click "Generate Term Sheet" to see the AI-generated result

The AI will analyze the lease and fill in the template with the extracted information.
