from flask import Flask, render_template, request, send_file, flash, redirect, url_for, session
import PyPDF2
from docx import Document
import io
import os
import google.generativeai as genai
from html.parser import HTMLParser
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class HTMLTextExtractor(HTMLParser):
    """Extract text content from HTML"""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = set()
        
    def handle_starttag(self, tag, attrs):
        # Skip content inside style and script tags
        if tag in ('style', 'script'):
            self.skip_tags.add(tag)
            
    def handle_endtag(self, tag):
        # Re-enable content extraction when closing style/script tags
        self.skip_tags.discard(tag)
        
    def handle_data(self, data):
        # Only add data if we're not inside a skip tag
        if not self.skip_tags and data.strip():
            self.text.append(data.strip())
        
    def get_text(self):
        return '\n'.join(self.text)

def read_html(file):
    """Extract text from HTML file
    
    Args:
        file: A file-like object (from user upload or opened file)
    """
    # Always expect a file-like object, never a path string
    html_content = file.read()
    if isinstance(html_content, bytes):
        html_content = html_content.decode('utf-8', errors='ignore')
    
    parser = HTMLTextExtractor()
    parser.feed(html_content)
    return parser.get_text()

def read_pdf(file):
    """Extract text from PDF file"""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def read_docx(file):
    """Extract text from DOCX file"""
    doc = Document(file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def read_document(file, filename):
    """Read document based on file type"""
    if filename.endswith('.pdf'):
        return read_pdf(file)
    elif filename.endswith('.docx'):
        return read_docx(file)
    elif filename.endswith('.htm') or filename.endswith('.html'):
        return read_html(file)
    else:
        return file.read().decode('utf-8')

def create_docx_from_text(text):
    """Create a DOCX document from text"""
    doc = Document()
    
    # Split text into lines and add to document
    lines = text.split('\n')
    for line in lines:
        doc.add_paragraph(line)
    
    # Save to BytesIO object
    docx_file = io.BytesIO()
    doc.save(docx_file)
    docx_file.seek(0)
    return docx_file

def list_available_models(api_key):
    """List available Gemini models"""
    try:
        genai.configure(api_key=api_key)
        models = []
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                models.append(model.name)
        return models
    except Exception as e:
        return []

# Load default template from file
def load_default_template():
    """Load the default template from Term Sheet Template_app.html"""
    template_path = os.path.join(os.path.dirname(__file__), "Term Sheet Template_app.html")
    try:
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8', errors='ignore') as f:
                return read_html(f)
        else:
            # Fallback to a basic template if file not found
            return """COMMERCIAL LEASE TERM SHEET

Property Address: [Address]
Tenant Name: [Tenant Name]
Landlord Name: [Landlord Name]

LEASE TERMS:

1. PREMISES
   - Suite/Unit Number: [Suite]
   - Rentable Square Feet: [SF]
   - Use: [Permitted Use]

2. LEASE TERM
   - Commencement Date: [Date]
   - Expiration Date: [Date]
   - Term Length: [Years/Months]
   - Option to Extend: [Yes/No, Terms]

3. BASE RENT
   - Initial Annual Base Rent: [Amount]
   - Monthly Base Rent: [Amount]
   - Rent Escalations: [Schedule]

4. ADDITIONAL RENT
   - Operating Expenses: [Details]
   - Property Taxes: [Details]
   - Utilities: [Responsibility]
   - CAM Charges: [Details]

5. SECURITY DEPOSIT
   - Amount: [Amount]
   - Terms: [Details]

6. TENANT IMPROVEMENTS
   - Tenant Improvement Allowance: [Amount]
   - Construction Period: [Timeline]

7. PARKING
   - Number of Spaces: [Number]
   - Type: [Reserved/Unreserved]
   - Cost: [Amount if any]

8. SPECIAL PROVISIONS
   - [Any special terms or conditions]

9. BROKER INFORMATION
   - Landlord's Broker: [Name]
   - Tenant's Broker: [Name]
"""
    except Exception as e:
        # Return fallback template if there's an error
        return """COMMERCIAL LEASE TERM SHEET

Property Address: [Address]
Tenant Name: [Tenant Name]
Landlord Name: [Landlord Name]

LEASE TERMS:

1. PREMISES
2. LEASE TERM
3. BASE RENT
4. ADDITIONAL RENT
5. SECURITY DEPOSIT
6. TENANT IMPROVEMENTS
7. PARKING
8. SPECIAL PROVISIONS
9. BROKER INFORMATION
"""

DEFAULT_TEMPLATE = load_default_template()

def generate_term_sheet(template_text, lease_text, api_key):
    """Generate term sheet using Gemini API"""
    
    prompt = f"""You are a commercial real estate expert. You have been provided with:
1. A lease term sheet template
2. A full commercial lease document

Your task is to analyze the commercial lease and extract all relevant information to create a completed lease term sheet that matches the template format exactly.

LEASE TERM SHEET TEMPLATE:
{template_text}

COMMERCIAL LEASE:
{lease_text}

Please generate a completed lease term sheet that:
1. Follows the exact structure and format of the template
2. Extracts all relevant information from the commercial lease
3. Fills in all sections of the template with appropriate data from the lease
4. Maintains professional formatting
5. Uses clear, concise language
6. If information is not found in the lease, indicate "Not specified in lease"

Generate the completed lease term sheet now:"""

    try:
        genai.configure(api_key=api_key)
        # Use gemini-2.5-pro for advanced lease analysis capabilities
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        full_prompt = f"""You are an expert commercial real estate attorney specializing in lease analysis and term sheet creation.

{prompt}"""
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=4000,
            )
        )
        return response.text
        
    except Exception as e:
        error_msg = str(e)
        # If model not found, try to list available models
        if "not found" in error_msg.lower() or "not supported" in error_msg.lower():
            available_models = list_available_models(api_key)
            if available_models:
                models_str = "\n".join([f"  - {m}" for m in available_models])
                return f"Error: The specified model is not available.\n\nAvailable models that support content generation:\n{models_str}\n\nOriginal error: {error_msg}"
            else:
                return f"Error generating term sheet: {error_msg}\n\nTip: Common model names include 'gemini-2.5-pro', 'gemini-1.5-flash', 'gemini-1.5-pro', or 'gemini-pro'"
        return f"Error generating term sheet: {error_msg}"

@app.route('/')
def index():
    """Home page with upload form"""
    # Get API key from environment variable or session
    default_api_key = os.environ.get('GEMINI_API_KEY')
    api_key_configured = default_api_key is not None or session.get('api_key') is not None
    
    return render_template('index.html', 
                         default_template_preview=DEFAULT_TEMPLATE[:1000],
                         api_key_configured=api_key_configured)

@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    """Set the API key in session"""
    api_key = request.form.get('api_key', '').strip()
    if api_key:
        session['api_key'] = api_key
        flash('API key set successfully!', 'success')
    else:
        flash('Please provide a valid API key.', 'error')
    return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate():
    """Generate term sheet from uploaded files"""
    # Get API key
    api_key = session.get('api_key') or os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        flash('Please configure your Gemini API key first.', 'error')
        return redirect(url_for('index'))
    
    # Check if lease file is uploaded
    if 'lease_file' not in request.files:
        flash('No lease file uploaded.', 'error')
        return redirect(url_for('index'))
    
    lease_file = request.files['lease_file']
    
    if lease_file.filename == '':
        flash('No lease file selected.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Read lease document
        lease_filename = secure_filename(lease_file.filename)
        lease_text = read_document(lease_file, lease_filename)
        
        # Get template text
        use_custom_template = request.form.get('use_custom_template') == 'on'
        
        if use_custom_template and 'template_file' in request.files:
            template_file = request.files['template_file']
            if template_file.filename != '':
                template_filename = secure_filename(template_file.filename)
                template_text = read_document(template_file, template_filename)
            else:
                template_text = DEFAULT_TEMPLATE
        else:
            template_text = DEFAULT_TEMPLATE
        
        # Generate term sheet
        term_sheet = generate_term_sheet(template_text, lease_text, api_key)
        
        # Store in session for display and download
        session['term_sheet'] = term_sheet
        session['lease_filename'] = lease_filename
        
        flash('Term sheet generated successfully!', 'success')
        return redirect(url_for('result'))
        
    except Exception as e:
        flash(f'Error processing documents: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/result')
def result():
    """Display the generated term sheet"""
    term_sheet = session.get('term_sheet')
    lease_filename = session.get('lease_filename', 'unknown')
    
    if not term_sheet:
        flash('No term sheet generated yet.', 'error')
        return redirect(url_for('index'))
    
    return render_template('result.html', 
                         term_sheet=term_sheet,
                         lease_filename=lease_filename)

@app.route('/download')
def download():
    """Download the generated term sheet as DOCX"""
    term_sheet = session.get('term_sheet')
    
    if not term_sheet:
        flash('No term sheet to download.', 'error')
        return redirect(url_for('index'))
    
    try:
        docx_file = create_docx_from_text(term_sheet)
        return send_file(
            docx_file,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name='lease_term_sheet.docx'
        )
    except Exception as e:
        flash(f'Error creating download: {str(e)}', 'error')
        return redirect(url_for('result'))

@app.route('/clear')
def clear():
    """Clear the session and start over"""
    session.pop('term_sheet', None)
    session.pop('lease_filename', None)
    flash('Session cleared. You can start a new analysis.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Only enable debug mode if explicitly set in environment
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
