import streamlit as st


if not st.user.is_logged_in:
    if st.button("Log in"):
        st.login("google")
else:
    if st.button("Log out"):
        st.logout()
    st.write(f"Hello, {st.user.name}!")


def login():
    if st.button("Log in"):
        st.user.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.user.logged_in = False
        st.rerun()


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
