import os
import re
from pathlib import Path

import streamlit as st
from pypdf import PdfReader

# Directory where PDF files are saved and analyzed
DOWNLOADS_DIR = Path("downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)

uploaded_file = st.file_uploader("Upload a scanned PDF", type=["pdf"])

def extract_text_from_pdf(file_path: Path) -> str:
    """Extracts all text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
        text += "\n"
    return text

def parse_info(text: str) -> dict:
    """Parse information like account number, email, and name from raw text."""
    info = {}

    account_match = re.search(r'Account Number[:\s]*([0-9\-xX*]+)', text, re.IGNORECASE)
    if account_match:
        info['account_number'] = account_match.group(1)

    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if email_match:
        info['email'] = email_match.group(0)

    name_match = re.search(r'Name[:\s]*([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)', text)
    if name_match:
        info['name'] = name_match.group(1)

    return info

def analyze_pdf(pdf_path: Path) -> dict:
    """Analyze a single PDF file and return parsed information."""
    try:
        text = extract_text_from_pdf(pdf_path)
        info = parse_info(text)
        return info
    except Exception as e:
        return {"error": str(e)}

def display_files_table():
    """Display a table of analyzed PDF files with a delete button for each."""
    pdf_files = list(DOWNLOADS_DIR.glob("*.pdf"))
    if not pdf_files:
        st.info("No PDF files uploaded yet.")
        return

    # Table header
    col1, col2, col3, col4, col5 = st.columns([3, 2, 3, 3, 1])
    col1.markdown(r"\*\*File\*\*")
    col2.markdown(r"\*\*Account\*\*")
    col3.markdown(r"\*\*Email\*\*")
    col4.markdown(r"\*\*Name\*\*")
    col5.markdown(r"\*\*Action\*\*")

    for pdf_file in pdf_files:
        info = analyze_pdf(pdf_file)
        file_name = pdf_file.name
        account = info.get("account_number", "N/A")
        email = info.get("email", "N/A")
        name = info.get("name", "N/A")

        col1, col2, col3, col4, col5 = st.columns([3, 2, 3, 3, 1])
        col1.write(file_name)
        col2.write(account)
        col3.write(email)
        col4.write(name)
        if col5.button("Delete", key=file_name):
            os.remove(pdf_file)
            st.success(f"Deleted file: {file_name}")
            st.rerun()

if uploaded_file is not None:
    # Save the uploaded file
    file_path = DOWNLOADS_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved: {uploaded_file.name}")
    st.rerun()

st.header("Analyzed PDF Files")
display_files_table()