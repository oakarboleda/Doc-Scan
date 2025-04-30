import json
import os

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from easyocr import Reader

UPLOAD_DIR = "downloads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text_from_image(image):
    reader = Reader(['en'])  # Initialize EasyOCR reader
    image_array = np.array(image)  # Convert PIL.Image to NumPy array
    result = reader.readtext(image_array, detail=0)
    return "\n".join(result)

def upload():
    upload_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg"])
    if upload_file is not None:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, upload_file.name)
        with open(file_path, "wb") as f:
            f.write(upload_file.getbuffer())
        st.success(f"File saved: {file_path}")

        # Extract text from the uploaded image
        image = Image.open(file_path)
        file_content = extract_text_from_image(image)

        # Save extracted text to a JSON file
        json_file_path = os.path.splitext(file_path)[0] + ".json"
        with open(json_file_path, "w") as json_file:
            json.dump({"text": file_content}, json_file, indent=2)
        st.success(f"JSON file created: {json_file_path}")

        # Save file content to session state
        st.session_state['file_content'] = file_content

    # Display saved files in a table
    files = os.listdir(UPLOAD_DIR)
    if files:
        st.write("Uploaded Files:")
        file_data = [{"File Name": f, "Path": os.path.join(UPLOAD_DIR, f)} for f in files]
        df = pd.DataFrame(file_data)
        st.dataframe(df)


upload()