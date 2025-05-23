import streamlit as st
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Constants
# SOME_FILE_PATH = "hello.txt"

st.set_page_config(
    page_icon="🛬", # use same icon for all pages
    layout="wide"
)

# Check authentication first (optional, see `auth.py`) - will stop execution if not authenticated
# check_auth()

# Setup navigation using st.Page
home = st.Page("pages/dashboard.py", title="Home", icon="🏠", default=True)
uploads = st.Page("pages/upload.py", title="Upload File", icon="🔁")
# authenticated = st.Page("pages/authenticated.py", title="Authenticated", icon="🔒")
pg = st.navigation([home, uploads])

# # render user info AFTER navigation setup
# render_user_info()

# Run the selected page
pg.run()