import streamlit as st
import pandas as pd
import os
from utils import load_css, menu

st.set_page_config(
    page_title="CU Timetable App",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "This is an automated timetable generator app for Covenant University.\n\n**FUN FACT:** It uses a hybrid of genetic algorithm and simulated annealing to generate a timetable for the university."
    }
)
menu()
load_css()

# Directory containing the Excel files
EXCEL_DIR = "../extracted_folder/master"

# Initialize session state variables
if 'active_page' not in st.session_state:
    st.session_state.active_page = 'file_list'
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None

# Function to list Excel files in the directory
def list_excel_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.xlsx')]

# Function to display the list of Excel files
def display_file_list():
    # st.image("assets/images/cu.png")
    st.title("Database Page")
    st.subheader("Programs")
    files = list_excel_files(EXCEL_DIR)
    for file in files:
        col1, col2 = st.columns([4, 1])

        with col2:
            file_path = os.path.join(EXCEL_DIR, file)
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"Download",
                    data=f,
                    file_name=file,
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
        with col1:
            if st.button(file):
                st.session_state.selected_file = file
                st.session_state.active_page = 'file_details'

# Function to display the sheets of the selected workbook
def display_file_details():
    # st.image("assets/images/cu.png")
    st.title(f"Program: {st.session_state.selected_file}")
    file_path = os.path.join(EXCEL_DIR, st.session_state.selected_file)
    excel_file = pd.ExcelFile(file_path)
    
    for sheet_name in excel_file.sheet_names:
        st.subheader(f"Level: {sheet_name}")
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        st.table(df)
    
    if st.button("Back"):
        st.session_state.active_page = 'file_list'
        st.session_state.selected_file = None

# Main application logic
if st.session_state.active_page == 'file_list':
    display_file_list()
elif st.session_state.active_page == 'file_details':
    display_file_details()