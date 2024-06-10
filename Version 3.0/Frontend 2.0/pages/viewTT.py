import streamlit as st
from utils import load_css, page_config, menu
import pandas as pd

page_config()
load_css()
menu()
# st.image("assets/images/cu.png")
st.title("View Timetable")

file_path = "C:/Users/USER/Documents/Important Files/Final Project/Version 3.0/sheets/final_timetable.xlsx"

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