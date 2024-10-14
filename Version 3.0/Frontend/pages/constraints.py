import streamlit as st
# import os, sys
# # Add the directory containing utils.py to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_css, menu
from datetime import timedelta

if "size" not in st.session_state:
    st.session_state.size = 20
    st.session_state.limit = "Time Limit"
    st.session_state.time = None
    st.session_state.max = None

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
st.session_state.size = st.number_input("Set population size: ", value=st.session_state.size)
size = st.session_state.size
st.divider()
st.subheader("SET COMPUTE LIMIT")
limit = st.radio(
    "What's the limit of the computation?",
    ["Time Limit", "Iteration Limit"],
    index=0 if st.session_state.limit == "Time Limit" else 1,
    captions=["Set the time limit in minutes.", "Set the max number of iterations."]
)
if limit == "Time Limit":
    st.session_state.limit = "Time Limit"
    st.session_state.time = st.time_input("Set time limit: ", value=st.session_state.time, step=180)
    if st.session_state.time:
        # Convert the time input to seconds
        total_seconds = timedelta(hours=st.session_state.time.hour, minutes=st.session_state.time.minute, seconds=st.session_state.time.second).total_seconds()
    st.write("Time limit is set for", st.session_state.time)
    st.session_state.max = None
    time = st.session_state.time
    max = st.session_state.max
else:
    st.session_state.limit = "Iteration Limit"
    st.session_state.time = None
    st.session_state.max = st.number_input("Set max number of iterations: ", value=st.session_state.max)
    time = st.session_state.time
    max = st.session_state.max
# set an if statement in the compute so if its none, nothing changes

def returnValues():
    return size, time, max