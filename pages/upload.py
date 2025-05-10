import re

import fitz  # PyMuPDF
import pytesseract
import streamlit as st
from PIL import Image


def clean_text(text):
    text = re.sub(r'[~\|✓→►•◦■¤©®™¨]', '', text)
    text = re.sub(r'\b(?:J-|SY|v|—|_~|~~|¥|“|”|‘|’|†)\b', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()


uploaded_file = st.file_uploader("Upload a scanned PDF", type=["pdf"])

if uploaded_file is not None:
    st.info("⏳ Processing PDF...")
    try:
        full_text = ""
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                pix = page.get_pixmap(dpi=300)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                full_text += pytesseract.image_to_string(img) + "\n"

        cleaned = clean_text(full_text)
        st.success("✅ Text extracted!")
        st.text_area("Extracted Text", cleaned, height=400)
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")