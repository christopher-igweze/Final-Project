import streamlit as st
from utils import load_css, page_config, menu

page_config()
load_css()
menu()

st.title("View Timetable")

file_path = "../extracted_folder/master/dataset_cleaned1.xlsx"

# Display download button
with open(file_path, "rb") as file:
    st.download_button(
        label="Download timetable",
        data=file,
        file_name="format.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )