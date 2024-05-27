import streamlit as st
from utils import load_css, page_config, menu

page_config()
load_css()
menu()

st.title("Constraints Page")
st.write("This page is for selecting constraints for the timetable generation.")