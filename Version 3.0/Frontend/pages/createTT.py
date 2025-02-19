import shutil
import streamlit as st
from utils import load_css, menu
import zipfile
import os
import subprocess

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

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'Upload Course Reg'

def store():
    if uploaded_file is not None: # UPLOADED FILE WAS DEFINED OUTSIDE THE FUNCTION
        # Delete any existing files or folders in the directory
        for file_name in os.listdir('../extracted_folder'):
            file_path = os.path.join('../extracted_folder', file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        # Unzip the uploaded file
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            zip_ref.extractall('../extracted_folder')

    # Populate the DB
    proc = subprocess.Popen(['python', 'C:/Users/USER/Documents/Important Files/Final Project/Version 3.0/Modules/db.py'], stdin=subprocess.PIPE)
    # Get the extracted folder path
    # extracted_folder = os.path.join('C:/Users/USER/Documents/Important Files/Final Project/Version 3.0', os.path.splitext(uploaded_file.name)[0])

# st.image("assets/images/cu.png")
st.header("Create a Timetable")

# Path to the specific file you want to provide for download
file_path = "../sheets/format.xlsx"
file_path2 = "../sheets/guide.txt"

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

# Display download button

with col1:
    with open(file_path, "rb") as file:
        st.download_button(
            label="Download format",
            data=file,
            file_name="format.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

with col2:
    with open(file_path2, "rb") as file:
        st.download_button(
            label="Download Guide",
            data=file,
            file_name="guide.txt",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

uploaded_file = st.file_uploader("Upload master.zip", type='zip', accept_multiple_files=False)

if "visibility" not in st.session_state:
    st.session_state.disabled = False
    option = st.selectbox(
        "What semester are you creating a timetable for?",
        ("Alpha", "Omega"),
        index=None,
        placeholder="Select a semester...",
    )

    alpha = True if option == "Alpha" else False

    if st.button("Create", key="create", disabled=not option or uploaded_file is None):
         store()
         with st.spinner('Creating timetable...'):
            proc = subprocess.Popen(['python', 'C:/Users/USER/Documents/Important Files/Final Project/Version 3.0/main.py'], stdin=subprocess.PIPE)
            proc.communicate(input=b'f\n')   

         st.success('Timetable finished. Navigate to timetable from the sidebar.')


# if st.button("test", key="test"):
#     with st.spinner('Creating timetable...'):
#         proc = subprocess.Popen(['python', 'C:/Users/USER/Documents/Important Files/Final Project/Version 3.0/main.py'], stdin=subprocess.PIPE)
#         proc.communicate(input=b'f\n')   

#     st.success('Timetable finished. Navigate to timetable from the sidebar.')
        
    

