import streamlit as st
import PyPDF2
from docx import Document
import io
import os
from openai import OpenAI
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

def generate_term_sheet(template_text, lease_text, api_key, api_provider):
    """Generate term sheet using OpenAI or Gemini API"""
    
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
        if api_provider == "OpenAI":
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert commercial real estate attorney specializing in lease analysis and term sheet creation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=4000
            )
            return response.choices[0].message.content
        
        elif api_provider == "Google Gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
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
    
    # API Key input
    st.sidebar.header("Configuration")
    
    # API Provider selection
    api_provider = st.sidebar.selectbox(
        "AI Provider",
        ["OpenAI", "Google Gemini"],
        help="Choose your AI provider"
    )
    
    # API Key input with dynamic label
    if api_provider == "OpenAI":
        api_key_label = "OpenAI API Key"
        api_key_help = "Enter your OpenAI API key to enable AI-powered analysis"
        api_link = "https://platform.openai.com/api-keys"
        api_link_text = "OpenAI"
    else:
        api_key_label = "Google Gemini API Key"
        api_key_help = "Enter your Google Gemini API key to enable AI-powered analysis"
        api_link = "https://makersuite.google.com/app/apikey"
        api_link_text = "Google AI Studio"
    
    api_key = st.sidebar.text_input(api_key_label, type="password", help=api_key_help)
    
    if not api_key:
        st.warning(f"⚠️ Please enter your {api_provider} API key in the sidebar to use this application.")
        st.info(f"""
        To use this application:
        1. Get an API key from [{api_link_text}]({api_link})
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
                    term_sheet = generate_term_sheet(template_text, lease_text, api_key, api_provider)
                    
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
