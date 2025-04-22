import streamlit as st

def login_screen():
    st.header("This app is private.")
    st.subheader("Please log in.")
    st.button("Log in with Google", on_click=st.login)

if not st.experimental_user.is_logged_in:
    login_screen()
else:
    st.header(f"Welcome, {st.experimental_user.name}!")
    st.button("Log out", on_click=st.logout)