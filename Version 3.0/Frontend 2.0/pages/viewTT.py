import streamlit as st
from utils import load_css, page_config, menu

page_config()
load_css()
menu()

st.title("View Timetable")
st.write("This page is for viewing the generated timetable.")