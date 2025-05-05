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

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
files = st.Page("pages/files.py", title="Files", icon=":material/folder:")
dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:")
profile = st.Page("pages/profile.py", title="Profile", icon=":material/account_circle:")
upload = st.Page("pages/upload.py", title="Upload", icon=":material/upload:")
analysis = st.Page("pages/analysis.py", title="analysis", icon=":material/bar_chart:")
history = st.Page("tools/history.py", title="History", icon=":material/history:")
# Main app logic
if st.session_state.logged_in:
    st.title("Welcome to the App!")
    pg = st.navigation(
        {
            "Dashboard": [dashboard],
            "Reports": [upload, files, analysis],
            "Tools": [history],
            "Account": [profile ],
        }
    )
else:
    st.title("Please log in to continue.")
    pg = st.navigation(
        {
            "Log in": [login_page],
        }
    )
    st.sidebar.write("Please log in to access the app.")
pg.run()
