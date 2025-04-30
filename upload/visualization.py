import pandas as pd
import streamlit as st
from awesome_table import AwesomeTable
from awesome_table.column import Column
def show_tables(tables, title=None):
    """
    Show tables in a grid format.
    """
    if title:
        st.title(title)

AwesomeTable(pd.json_normalize(data), columns=[
    Column(name='id', label='ID'),
    Column(name='name', label='Name'),
    Column(name='job_title', label='Job Title'),
    Column(name='avatar', label='Avatar'),
    Column(name='_url.social_media', label='Social Media'),
    Column(name='_url.document', label='Document'),
])