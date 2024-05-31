import streamlit as st
from json import load
import streamlit as st
import yaml, os
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

path = os.path.join(os.path.dirname(__file__), 'config.yaml')

with open(path) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

def load_css():
    with open("assets/styles/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def menu():
    st.sidebar.page_link("app.py", label="🏡 Home")
    st.sidebar.page_link("pages/db.py", label="📂 Database")
    st.sidebar.page_link("pages/createTT.py", label="🔨 Create Timetable")
    st.sidebar.page_link("pages/viewTT.py", label="📄 View Timetable")
    st.sidebar.page_link("pages/constraints.py", label="🔒 Constraints")
    st.sidebar.page_link("pages/profile.py", label="🧙🏼‍♂️ Profile")
    # st.sidebar.markdown("---")
    # if st.sidebar.button("Logout", key="logoutbutton", type="secondary"):
    #     authenticator.logout()
    #     st.switch_page("app.py")


def page_config():
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