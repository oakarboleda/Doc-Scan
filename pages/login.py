import streamlit as st


def login():
    st.title("Login")

    st.write("This is the login page.")
    # Add your login content here
    st.button("Login", on_click=: st.session_state.clear())
