import re
import json
import re
from pathlib import Path

import streamlit as st
from pypdf import \
    PdfReader  # Make sure you installed with: pip install pypdf# Make sure you installed with: pip install pypdf

uploaded_file = st.file_uploader("Upload a scanned PDF", type=["pdf"])

def extract_text_from_pdf(file_path: Path) -> str:
    """Extracts all text from a PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""  # In case a page has no extractable text
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

def analyze_pdfs_in_directory(input_dir: Path):
    """Loop through PDF files in a directory and analyze them."""
    for pdf_file in input_dir.glob("*.pdf"):
        print(f"Analyzing: {pdf_file.name}")
        text = extract_text_from_pdf(pdf_file)
        parsed_info = parse_info(text)

        print(json.dumps(parsed_info, indent=2))
        print("-" * 40)

def main():
    input_dir = Path("downloads")  # Change this to your actual folder path if needed
    if not input_dir.exists():
        print(f"Directory {input_dir} does not exist. Please create it and add PDF files.")
        return

    analyze_pdfs_in_directory(input_dir)

if __name__ == "__main__":
    main()