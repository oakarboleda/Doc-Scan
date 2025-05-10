import streamlit as st

dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:")
upload = st.Page("pages/upload.py", title="Upload", icon=":material/upload:")
# analysis = st.Page("pages/analysis.py", title="analysis", icon=":material/bar_chart:")
# Main app logic

    pg = st.navigation(
        {
            "Dashboard": [dashboard],
            "Actions": [upload],
            "Logout": [st.logout]

        }
    )



