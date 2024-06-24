import streamlit as st
from utils import load_css, menu
from datetime import timedelta

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
st.write("This page is for setting some constraints for the timetable generation.")
st.divider()
st.subheader("SET POPULATION SIZE")
size = st.number_input("Set population size: ", value=20)
st.divider()
st.subheader("SET COMPUTE LIMIT")
limit = st.radio(
    "What's the limit of the computation?",
    ["Time Limit", "Iteration Limit"],
    captions = ["Set the time limit in minutes.", "Set the max number of iterations."]
)
if limit == "Time Limit":
    time = st.time_input("Set time limit: ", value=None, step=180)
    if time:
        # Convert the time input to seconds
        total_seconds = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second).total_seconds()
    st.write("Time limit is set for", time)
    max = None
else:
    time = None
    max = st.number_input("Set max number of iterations: ", value=None)

# set an if statement in the compute so if its none, nothing changes