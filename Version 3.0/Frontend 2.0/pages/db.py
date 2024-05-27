import streamlit as st
from utils import load_css, menu, page_config

page_config()
menu()
load_css()
st.title("Database Page")
st.write("Welcome to the database page. This is the first page of your menu.")