import streamlit as st
from utils import guestMenu, load_css, menu
import pandas as pd

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
guestMenu()
# st.image("assets/images/cu.png")
st.title("View Timetable")


file_path = "../sheets/final_timetable.xlsx"

# Display download button
with open(file_path, "rb") as file:
    st.download_button(
        label="Download timetable",
        data=file,
        file_name="Timetable.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Read the excel file
    df = pd.read_excel(file_path, sheet_name=None)

    # Display all sheets
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for sheet_name, day in zip(df.keys(), days_of_week):
        st.write(f"Day: {day}")
        st.write(df[sheet_name])