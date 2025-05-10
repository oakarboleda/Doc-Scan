import streamlit as st


def logout():
    st.session_state.role = None
    st.rerun()



logout()