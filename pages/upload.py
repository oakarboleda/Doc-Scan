import os
import re
from pathlib import Path

import fitz  # PyMuPDF
import streamlit as st

# Directory where PDF files are saved and analyzed
DOWNLOADS_DIR = Path("downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)

uploaded_file = st.file_uploader("Upload a scanned PDF", type=["pdf"])

def extract_text_natively(file_path: Path) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_info(text: str) -> dict:
    """Parse information like account number, email, and name from raw text."""
    info = {}

    account_match = re.search(r'Account Number[:\s]*([0-9\-xX*]+)', text, re.IGNORECASE)
    if account_match:
        info['account_number'] = account_match.group(1)

    invoice_match = re.search(r'Invoice Number[:\s]*([0-9]+)', text, re.IGNORECASE)
    if invoice_match:
        info['invoice_number'] = invoice_match.group(1)

    billing_date_match = re.search(r'Billing Date[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})', text, re.IGNORECASE)
    if billing_date_match:
        info['billing_date'] = billing_date_match.group(1)

    due_date_match = re.search(r'Due Date[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})', text, re.IGNORECASE)
    if due_date_match:
        info['due_date'] = due_date_match.group(1)

    company_match = re.search(r'^(Northern Utilities Co\.)\s+([\w\s.,]+Minneapolis,\s+MN\s+\d{5})', text, re.MULTILINE)
    if company_match:
        info['company_name'] = company_match.group(1)
        info['company_address'] = company_match.group(2)

    return info

def analyze_pdf(pdf_path: Path) -> dict:
    """Analyze a single PDF file and return parsed information."""
    try:
        text = extract_text_natively(pdf_path)
        info = parse_info(text)
        return {"info": info, "text": text}
    except Exception as e:
        return {"error": str(e)}

def display_files_table():
    """Display a table of analyzed PDF files with a delete button for each."""
    pdf_files = list(DOWNLOADS_DIR.glob("*.pdf"))
    if not pdf_files:
        st.info("No PDF files uploaded yet.")
        return

    # Table header
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2.5, 2.5, 2.5, 2.5, 2.5, 3, 3, 1])
    col1.markdown("**File**")
    col2.markdown("**Account**")
    col3.markdown("**Invoice**")
    col4.markdown("**Billing**")
    col5.markdown("**Due**")
    col6.markdown("**Company**")
    col7.markdown("**Address**")
    col8.markdown("**Action**")

    for pdf_file in pdf_files:
        result = analyze_pdf(pdf_file)
        if "error" in result:
            parsed_info = {}
            raw_text = result["error"]
        else:
            parsed_info = result.get("info", {})
            raw_text = result.get("text", "")
        file_name = pdf_file.name

        account = parsed_info.get("account_number", "N/A")
        invoice = parsed_info.get("invoice_number", "N/A")
        billing = parsed_info.get("billing_date", "N/A")
        due = parsed_info.get("due_date", "N/A")
        company = parsed_info.get("company_name", "N/A")
        address = parsed_info.get("company_address", "N/A")

        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([2.5, 2.5, 2.5, 2.5, 2.5, 3, 3, 1])
        col1.write(file_name)
        col2.write(account)
        col3.write(invoice)
        col4.write(billing)
        col5.write(due)
        col6.write(company)
        col7.write(address)
        if col8.button("Delete", key=file_name):
            os.remove(pdf_file)
            st.success(f"Deleted file: {file_name}")
            st.rerun()
        with st.expander("Show parsed text", expanded=False):
            st.text_area("Raw Text", value=raw_text, height=200)

if uploaded_file is not None:
    # Save the uploaded file
    file_path = DOWNLOADS_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved: {uploaded_file.name}")
    st.rerun()

st.header("Analyzed PDF Files")
display_files_table()