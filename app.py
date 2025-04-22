import streamlit as st

def login_screen():
    st.header("Login")
    st.subheader("Please log in to access the app")
    st.button("Login with Google", on_click=st.login)

    if not st.experimental_user.is_logged_in:
        login_screen()
    else:
        st.header(f"Welcome, {st.experimental_user.name}")
        st.button("Logout", on_click=st.logout, key="logout")




