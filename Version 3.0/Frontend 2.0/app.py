import streamlit as st
from utils import load_css, page_config
import yaml, os
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

page_config()

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
        config['cookie']['expiry_days'],
        config['pre-authorized']
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