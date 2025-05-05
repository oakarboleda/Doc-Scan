# Required packages:
# pip install pymupdf easyocr pillow numpy
import os
import re

import dotenv
import easyocr
import fitz  # PyMuPDF
import numpy as np
import streamlit as st
from PIL import Image

dotenv.load_dotenv()

def analysis():
    selected_file = st.session_state.get('selected_file')
    if selected_file:
        st.write(f"Analyzing file: {os.path.basename(selected_file)}")

        with st.spinner("Processing the file..."):
            file_path = os.path.join("../downloads", selected_file)
            try:
                if selected_file.lower().endswith('.pdf'):
                    doc = fitz.open(file_path)
                    reader = easyocr.Reader(['en'])
                    page_count = len(doc)
                    st.info(f"PDF contains {page_count} page{'s' if page_count != 1 else ''}. Processing all pages...")
                    pages_data = []

                    for page_num in range(page_count):
                        page = doc.load_page(page_num)
                        pix = page.get_pixmap()
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        img_np = np.array(img)
                        result = reader.readtext(img_np, detail=0)
                        raw_text = " ".join(result)

                        # Clean text
                        cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', raw_text)
                        cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)
                        cleaned_text = re.sub(r'\n{2,}', '\n', cleaned_text).strip()

                        # Extract structured data
                        structured_data = {}

                        account_match = re.search(r'Account(?: Number)?[:\s#]*([0-9xX\-\*]{6,})', cleaned_text, re.IGNORECASE)
                        if account_match:
                            structured_data['account_number'] = account_match.group(1)

                        balance_match = re.search(r'(?:Balance\s+Due|Amount\s+Due)[:\s$]*([0-9,]+\.\d{2})', cleaned_text, re.IGNORECASE)
                        if balance_match:
                            structured_data['balance'] = balance_match.group(1)

                        name_match = re.search(r'Dear\s+([A-Z][a-z]+\s+[A-Z][a-z]+)', cleaned_text)
                        if name_match:
                            structured_data['name'] = name_match.group(1)

                        address_match = re.search(r'\d{3,5}\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s+[A-Z]{2}\s+\d{5}', cleaned_text)
                        if address_match:
                            structured_data['address'] = address_match.group(0)

                        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', cleaned_text)
                        if email_match:
                            structured_data['email'] = email_match.group(0)

                        pages_data.append({
                            "page_number": page_num + 1,
                            "structured_data": structured_data,
                            "cleaned_text": cleaned_text
                        })

                    st.success(f"Finished processing {page_count} page{'s' if page_count != 1 else ''}.")

                    for page_data in pages_data:
                        with st.expander(f"Page {page_data['page_number']}"):
                            st.subheader("Extracted Information")
                            st.json(page_data["structured_data"])
                            st.subheader("Cleaned OCR Text")
                            st.text_area("OCR Output", page_data["cleaned_text"], height=400)

                else:
                    st.warning("Unsupported file type for analysis.")
            except Exception as e:
                st.error(f"Error during analysis: {e}")
    else:
        st.warning("No file selected for analysis.")

analysis()