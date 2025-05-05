import streamlit as st
from st_pages import add_page_title, get_nav_from_toml


nav = get_nav_from_toml()


pg = st.navigation(nav)

add_page_title(pg)

pg.run()