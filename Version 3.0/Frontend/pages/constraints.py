import streamlit as st
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
load_css()
menu()
# st.image("assets/images/cu.png")
st.title("Constraints Page")
st.write("This page is for selecting constraints for the timetable generation.")