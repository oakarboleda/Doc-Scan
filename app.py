import streamlit as st


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

st.sidebar.button("Log Out", on_click=logout)


dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:")
upload = st.Page("pages/upload.py", title="Upload", icon=":material/upload:")
# analysis = st.Page("pages/analysis.py", title="analysis", icon=":material/bar_chart:")
# Main app logic
if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Dashboard": [dashboard],
            "Reports": [upload]

        }
    )
else:
    st.title("Please log in to continue.")
    st.button("Log in", on_click=login)

if st.session_state.logged_out:
    st.session_state.logged_out = true
    st.session_state.logged_in = False
    st.session_state.clear()

pg.run()
