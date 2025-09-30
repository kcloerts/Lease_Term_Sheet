import streamlit as st
import PyPDF2
from docx import Document
import io
import os
import google.generativeai as genai

# Set page configuration
st.set_page_config(
    page_title="Lease Term Sheet Generator",
    page_icon="📄",
    layout="wide"
)

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

def read_document(file):
    """Read document based on file type"""
    if file.name.endswith('.pdf'):
        return read_pdf(file)
    elif file.name.endswith('.docx'):
        return read_docx(file)
    else:
        return file.read().decode('utf-8')

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
        model = genai.GenerativeModel('gemini-1.5-flash')
        
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
        return f"Error generating term sheet: {str(e)}"

# Main app
def main():
    st.title("📄 Lease Term Sheet Generator")
    st.markdown("""
    This application helps you generate a lease term sheet by analyzing a commercial lease document 
    and matching it to your template format.
    """)
    
    # API Key configuration
    st.sidebar.header("Configuration")
    
    # Try to get default API key from secrets
    default_api_key = None
    try:
        if hasattr(st, 'secrets') and 'gemini' in st.secrets and 'api_key' in st.secrets['gemini']:
            default_api_key = st.secrets['gemini']['api_key']
    except Exception:
        pass
    
    # API Key input - optional if default is available
    if default_api_key:
        st.sidebar.success("✅ Using default Gemini API key")
        use_custom_key = st.sidebar.checkbox("Use custom API key", value=False)
        if use_custom_key:
            api_key = st.sidebar.text_input(
                "Google Gemini API Key", 
                type="password",
                help="Enter your Google Gemini API key to override the default"
            )
            if not api_key:
                api_key = default_api_key
        else:
            api_key = default_api_key
    else:
        st.sidebar.info("💡 No default API key configured")
        api_key = st.sidebar.text_input(
            "Google Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key to enable AI-powered analysis"
        )
    
    if not api_key:
        st.warning("⚠️ Please enter your Google Gemini API key in the sidebar to use this application.")
        st.info("""
        To use this application:
        1. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Enter it in the sidebar
        3. Upload your documents
        """)
        return
    
    # Create two columns for file uploads
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1️⃣ Upload Lease Term Sheet Template")
        template_file = st.file_uploader(
            "Upload template (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt'],
            key="template",
            help="Upload your lease term sheet template that will be used as the format"
        )
        
        if template_file:
            st.success(f"✅ Template uploaded: {template_file.name}")
    
    with col2:
        st.subheader("2️⃣ Upload Commercial Lease")
        lease_file = st.file_uploader(
            "Upload lease (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt'],
            key="lease",
            help="Upload the commercial lease document to analyze"
        )
        
        if lease_file:
            st.success(f"✅ Lease uploaded: {lease_file.name}")
    
    # Process documents when both are uploaded
    if template_file and lease_file:
        st.markdown("---")
        
        if st.button("🚀 Generate Term Sheet", type="primary"):
            with st.spinner("Reading documents..."):
                try:
                    # Read both documents
                    template_text = read_document(template_file)
                    lease_text = read_document(lease_file)
                    
                    st.success("✅ Documents read successfully!")
                    
                    # Show preview in expanders
                    with st.expander("📄 View Template Preview"):
                        st.text_area("Template Content", template_text[:2000] + "..." if len(template_text) > 2000 else template_text, height=200, disabled=True)
                    
                    with st.expander("📄 View Lease Preview"):
                        st.text_area("Lease Content", lease_text[:2000] + "..." if len(lease_text) > 2000 else lease_text, height=200, disabled=True)
                    
                except Exception as e:
                    st.error(f"❌ Error reading documents: {str(e)}")
                    return
            
            with st.spinner("🤖 Analyzing lease and generating term sheet... This may take 30-60 seconds."):
                try:
                    # Generate term sheet
                    term_sheet = generate_term_sheet(template_text, lease_text, api_key)
                    
                    st.success("✅ Term sheet generated successfully!")
                    
                    # Display result
                    st.markdown("---")
                    st.subheader("📋 Generated Lease Term Sheet")
                    st.markdown(term_sheet)
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Term Sheet",
                        data=term_sheet,
                        file_name="lease_term_sheet.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error generating term sheet: {str(e)}")
    else:
        st.info("👆 Please upload both a template and a lease document to begin.")

if __name__ == "__main__":
    main()
