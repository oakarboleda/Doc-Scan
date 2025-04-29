import streamlit as st
from PIL import Image
from PyPDF2 import PdfReader
from docx import Document
from dotenv import load_dotenv
from easyocr import Reader

# Load environment variables from .env file
load_dotenv()

def extract_text_from_image(image):
    reader = Reader(['en'])  # Initialize EasyOCR reader
    result = reader.readtext(image, detail=0)
    return " ".join(result)

def extract_text_from_doc(doc_file):
    document = Document(doc_file)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def upload():
    upload_file = st.file_uploader("Choose a file", type=["doc", "docx", "png", "jpg", "jpeg", "pdf"])
    if upload_file is not None:
        if upload_file.name.endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(upload_file)
            file_content = extract_text_from_image(image)
        elif upload_file.name.endswith((".doc", ".docx")):
            file_content = extract_text_from_doc(upload_file)
        elif upload_file.name.endswith(".pdf"):
            file_content = extract_text_from_pdf(upload_file)
        else:
            file_content = "Unsupported file type."

        st.text_area("File Content", file_content, height=300)

        if st.button("Parse Information"):
            with st.spinner("Parsing information..."):
                st.subheader("Parsed Information")
                st.write(file_content)

upload()