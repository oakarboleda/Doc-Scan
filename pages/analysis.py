# import json
# import math
# import os
#
# import streamlit as st
# import streamlit_javascript as st_js
# from PIL import Image
# from streamlit_sparrow_labeling import st_sparrow_labeling, DataProcessor
#
# UPLOAD_DIR = "./uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)
#
# # Display saved files in a table
# files = os.listdir(UPLOAD_DIR)
# if files:
#     selected_file = st.selectbox("Select a document", files)
#     if st.button("Load Document"):
#         img_file = os.path.join(UPLOAD_DIR, selected_file)
#         rects_file = os.path.splitext(img_file)[0] + ".json"
#         if os.path.exists(img_file) and os.path.exists(rects_file):
#             st.session_state['selected_file'] = img_file
#             st.success(f"Selected file: {selected_file}")
#         else:
#             st.error("Selected file or its corresponding JSON file does not exist.")
# else:
#     st.warning("No files available in the directory.")
#
# def run(img_file, rects_file, labels):
#     ui_width = st_js.st_javascript("window.innerWidth")
#
#     try:
#         docImg = Image.open(img_file)
#     except FileNotFoundError:
#         st.error("Image file not found.")
#         return
#
#     saved_state = st.session_state.get('saved_state')
#     if not saved_state:
#         try:
#             with open(rects_file, "r") as f:
#                 saved_state = json.load(f)
#                 st.session_state['saved_state'] = saved_state
#         except (FileNotFoundError, json.JSONDecodeError) as e:
#             st.error(f"Error loading file: {e}")
#             return
#
#     assign_labels = st.checkbox("Assign Labels", True)
#     mode = "transform" if assign_labels else "rect"
#
#     data_processor = DataProcessor()
#
#     col1, col2 = st.columns([4, 6])
#
#     with col1:
#         height = saved_state['meta']['image_size']['height']
#         width = saved_state['meta']['image_size']['width']
#
#         canvas_width = canvas_available_width(ui_width)
#
#         result_rects = st_sparrow_labeling(
#             fill_color="rgba(0, 151, 255, 0.3)",
#             stroke_width=2,
#             stroke_color="rgba(0, 50, 255, 0.7)",
#             background_image=docImg,
#             initial_rects=saved_state,
#             height=height,
#             width=width,
#             drawing_mode=mode,
#             display_toolbar=True,
#             update_streamlit=True,
#             canvas_width=canvas_width,
#             doc_height=height,
#             doc_width=width,
#             image_rescale=True,
#             key="doc_annotation"
#         )
#
#         st.caption("Check 'Assign Labels' to enable editing of labels and values, move and resize the boxes to "
#                    "annotate the document.")
#         st.caption("Add annotations by clicking and dragging on the document, when 'Assign Labels' is unchecked.")
#
#     with col2:
#         if result_rects is not None:
#             with st.form(key="fields_form"):
#                 if result_rects.current_rect_index is not None and result_rects.current_rect_index != -1:
#                     st.write("Selected Field: ",
#                              result_rects.rects_data['words'][result_rects.current_rect_index]['value'])
#                     st.markdown("---")
#
#                 if ui_width > 1500:
#                     render_form_wide(result_rects.rects_data['words'], labels, result_rects, data_processor)
#                 elif ui_width > 1000:
#                     render_form_avg(result_rects.rects_data['words'], labels, result_rects, data_processor)
#                 elif ui_width > 500:
#                     render_form_narrow(result_rects.rects_data['words'], labels, result_rects, data_processor)
#                 else:
#                     render_form_mobile(result_rects.rects_data['words'], labels, result_rects, data_processor)
#
#                 submit = st.form_submit_button("Save", type="primary")
#                 if submit:
#                     try:
#                         with open(rects_file, "w") as f:
#                             json.dump(result_rects.rects_data, f, indent=2)
#                         with open(rects_file, "r") as f:
#                             saved_state = json.load(f)
#                             st.session_state['saved_state'] = saved_state
#                         st.write("Saved!")
#                     except Exception as e:
#                         st.error(f"Error saving file: {e}")
#
# def canvas_available_width(ui_width):
#     if ui_width > 500:
#         return math.floor(38 * ui_width / 100)
#     else:
#         return ui_width
#
# if 'selected_file' in st.session_state:
#     selected_file = st.session_state['selected_file']
#     img_file = selected_file
#     rects_file = os.path.splitext(selected_file)[0] + ".json"
#     labels = ["", "item", "item_price", "subtotal", "tax", "total"]
#
#     if os.path.exists(img_file) and os.path.exists(rects_file):
#         run(img_file, rects_file, labels)
#     else:
#         st.error("Selected file or its corresponding JSON file does not exist.")
# else:
#     st.warning("No file selected. Please upload and select a file first.")