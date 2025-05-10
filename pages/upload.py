import json
import os

import numpy as np
import streamlit as st
from PIL import Image
from easyocr import Reader
from pypdf import PdfReader

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text_from_image(image):
    reader = Reader(['en'])  # Initialize EasyOCR reader
    image_array = np.array(image)  # Convert PIL.Image to NumPy array
    result = reader.readtext(image_array, detail=0)
    return "\n".join(result)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file using PyPDF2."""
    text = ""
    with open(pdf_path, "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def upload():
    upload_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg", "pdf"])
    if upload_file is not None:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, upload_file.name)
        with open(file_path, "wb") as f:
            f.write(upload_file.getbuffer())
        st.success(f"File saved: {file_path}")

        # Process the file based on its type
        if upload_file.name.endswith(".pdf"):
            file_content = extract_text_from_pdf(file_path)
        elif upload_file.name.lower().endswith((".png", ".jpg", ".jpeg")):
            image = Image.open(file_path)
            file_content = extract_text_from_image(image)
        else:
            st.error("Unsupported file type.")
            return

            # Save extracted text to a JSON file
            json_file_path = os.path.splitext(file_path)[0] + ".json"
            with open(json_file_path, "w") as json_file:
                json.dump({"text": file_content}, json_file, indent=2)
            st.success(f"JSON file created: {json_file_path}")

            # Save file content to session state
            st.session_state['file_content'] = file_content

        # Display saved files in a table with preview and delete buttons
    files = os.listdir(UPLOAD_DIR)
    if files:
        st.write("Uploaded Files:")
        for file_name in files:
            file_path = os.path.join(UPLOAD_DIR, file_name)
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(file_name)
            with col2:
                if st.button("Preview", key=f"preview_{file_name}"):
                    if file_name.endswith(".pdf"):
                        text = extract_text_from_pdf(file_path)
                        st.text_area("Preview (PDF Text):", text, height=200)
                    elif file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                        image = Image.open(file_path)
                        st.image(image, caption=file_name, use_column_width=True)
                    else:
                        st.error("Preview not supported for this file type.")
            with col3:
                if st.button("Delete", key=f"delete_{file_name}"):
                    os.remove(file_path)
                    st.success(f"Deleted file: {file_name}")
                    st.rerun()
            with col4:
                if st.button("Analyze", key=f"analyze_{file_name}"):
                    st.session_state['selected_file'] = file_path
                    st.success(f"File selected for analysis: {file_name}")
                    st.experimental_set_query_params(page="analysis")
                    st.rerun()

upload()
st.title("Upload Files")
st.write("Upload your files for analysis.")
upload_file()
display_uploaded_files()

if __name__ == "__main__":
    upload()