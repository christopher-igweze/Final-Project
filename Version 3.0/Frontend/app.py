import streamlit as st
from utils import load_css
import yaml, os
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

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

def index_page():
    load_css()
    st.image("assets/images/updatedcu2.png")  # Replace with your image path


    path = os.path.join(os.path.dirname(__file__), 'config.yaml')

    with open(path) as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    # Authenticating Users
    if st.session_state["authentication_status"]:
        if st.button("Create new timetable", use_container_width=True):
            st.switch_page("pages/createTT.py")
    elif st.session_state["authentication_status"] is None:
        if st.button("Login", use_container_width=True):
            st.switch_page("pages/login.py")

if __name__ == "__main__":
    index_page()