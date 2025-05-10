# language: python
import os

import streamlit as st

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def files():
    st.title("Uploaded Files")

    # Add a file uploader for supporting png, jpg, jpeg and pdf
    uploaded = st.file_uploader("Upload a file", type=["png", "jpg", "jpeg", "pdf"], key="files-upload")
    if uploaded is not None:
        file_path = os.path.join(UPLOAD_DIR, uploaded.name)
        with open(file_path, "wb") as f:
            f.write(uploaded.getbuffer())
        st.success(f"File saved: {uploaded.name}")
        st.experimental_rerun()  # Refresh the file list

    # List existing files and provide a delete button for each
    if os.path.exists(UPLOAD_DIR):
        files = os.listdir(UPLOAD_DIR)
        if files:
            for file in files:
                file_path = os.path.join(UPLOAD_DIR, file)
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(file)
                with col2:
                    if st.button("Delete", key=file):
                        os.remove(file_path)
                        st.success(f"Deleted file: {file}")
                        st.rerun()  # Refresh the app to update the file list
        else:
            st.info("No files have been uploaded yet.")
    else:
        st.error(f"The directory \\`{UPLOAD_DIR}\\` does not exist.")

files()