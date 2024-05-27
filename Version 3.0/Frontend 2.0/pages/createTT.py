import streamlit as st
from utils import load_css, page_config, menu

page_config()
menu()
load_css()
st.title("Create Timetable")
st.write("Welcome to the database page. This is the first page of your menu.")