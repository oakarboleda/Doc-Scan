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

                        # Start structured_data with default type
                        structured_data = {
                            "document_type": "Unknown"
                        }

                        # IONOS Invoice Detection and Extraction
                        if "Invoice" in cleaned_text and "IONOS" in cleaned_text:
                            structured_data["document_type"] = "IONOS Invoice"

                            invoice_no = re.search(r"Invoice[:\s#]*([0-9]{9,})", cleaned_text)
                            if invoice_no:
                                structured_data["invoice_number"] = invoice_no.group(1)

                            invoice_date = re.search(r"Invoice Date[:\s]+([0-9/]+)", cleaned_text)
                            if invoice_date:
                                structured_data["invoice_date"] = invoice_date.group(1)

                            customer_id = re.search(r"Customer ID[:\s]+([0-9]+)", cleaned_text)
                            if customer_id:
                                structured_data["customer_id"] = customer_id.group(1)

                            contract_id = re.search(r"Contract ID[:\s]+([0-9]+)", cleaned_text)
                            if contract_id:
                                structured_data["contract_id"] = contract_id.group(1)

                            total_due = re.search(r"Total amount due.*?\$([0-9]+\.[0-9]{2})", cleaned_text,
                                                  re.IGNORECASE)
                            if total_due:
                                structured_data["total_due"] = total_due.group(1)

                        match = re.search(r'Account Number[:\s]+([0-9\-xX*]+)', cleaned_text, flags=re.IGNORECASE)
                        if match:
                            structured_data['account_number'] = match.group(1)

                        balance_match = re.search(r'(?:Balance\s+Due|Amount\s+Due)[:\s$]*([0-9,]+\.\d{2})', cleaned_text, flags=re.IGNORECASE)
                        if balance_match:
                            structured_data['balance'] = balance_match.group(1)

                        name_match = re.search(r'Dear\s+([A-Z][a-z]+\s+[A-Z][a-z]+)', cleaned_text)
                        if name_match:
                            structured_data['name'] = name_match.group(1)

                        address_match = re.search(r'\d{3,5}\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s+[A-Z]{2}\s+\d{5}', cleaned_text, flags=re.IGNORECASE)
                        if address_match:
                            structured_data['address'] = address_match.group(0)

                        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', cleaned_text)
                        if email_match:
                            structured_data['email'] = email_match.group(0)

                        # Optionally split into logical document sections
                        sections = re.split(r'(?=REPAYMENT SCHEDULE|COLLECTION NOTICE|MINNESOTA REVENUE)', cleaned_text, flags=re.IGNORECASE)
                        sectioned_text = []
                        for section in sections:
                            section = section.strip()
                            if section:
                                sectioned_text.append(section)

                        pages_data.append({
                            "page_number": page_num + 1,
                            "structured_data": structured_data,
                            "cleaned_text": cleaned_text,
                            "sectioned_text": sectioned_text
                        })

                    st.success(f"Finished processing {page_count} page{'s' if page_count != 1 else ''}.")

                    for page_data in pages_data:
                        with st.expander(f"Page {page_data['page_number']}"):
                            st.subheader("Extracted Information")
                            st.json(page_data["structured_data"])
                            st.subheader("Cleaned OCR Text")
                            # Display each section in a collapsible Streamlit expander
                            for idx, section in enumerate(page_data.get("sectioned_text", []), 1):
                                with st.expander(f"Section {idx}"):
                                    st.text(section)

                else:
                    st.warning("Unsupported file type for analysis.")
            except Exception as e:
                st.error(f"Error during analysis: {e}")
    else:
        st.warning("No file selected for analysis.")

analysis()