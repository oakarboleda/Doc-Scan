# import os
#
# import streamlit as st
#
# UPLOAD_DIR = "../downloads"
#
# def files():
#     st.title("Uploaded Files")
#
#     # Check if the directory exists and list files
#     if os.path.exists(UPLOAD_DIR):
#         files = os.listdir(UPLOAD_DIR)
#         if files:
#             for file in files:
#                 file_path = os.path.join(UPLOAD_DIR, file)
#                 col1, col2 = st.columns([4, 1])
#                 with col1:
#                     st.write(file)
#                 with col2:
#                     if st.button("Delete", key=file):
#                         os.remove(file_path)
#                         st.success(f"Deleted file: {file}")
#                         st.rerun()  # Refresh the app to update the file list
#         else:
#             st.info("No files have been uploaded yet.")
#     else:
#         st.error(f"The directory '{UPLOAD_DIR}' does not exist.")
#
# files()