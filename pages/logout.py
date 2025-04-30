import streamlit as st


def logout():
    st.title("Logout")
    st.write("You have been logged out.")
    # Add your logout content here
    st.button("Login Again", on_click=lambda: st.session_state.clear())




logout()