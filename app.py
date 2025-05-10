import streamlit as st



def login_screen():
    st.header("This app is private.")
    st.subheader("Please log in.")
    st.button("Log in with Google", on_click=st.login)

if not st.user.is_logged_in:
    login_screen()
else:
    st.header(f"Welcome, {st.user.name}!")
    st.button("Log out", on_click=st.logout)


dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:")
upload = st.Page("pages/upload.py", title="Upload", icon=":material/upload:")
# analysis = st.Page("pages/analysis.py", title="analysis", icon=":material/bar_chart:")
# Main app logic
if st.user.logged_in:
    pg = st.navigation(
        {
            "Dashboard": [dashboard],
            "Actions": [upload],
            "Logout": [logout]

        }
    )
else:
    pg = st.navigation(
        {
            "Login": [login]
        }
    )





pg.run()
