from pages import st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
# from Frontend.app import page


# Creating a login widget
path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')

with open(path) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login() # to render the login form

# Authenticating Users
if st.session_state["authentication_status"]:
    st.switch_page("pages/db_page.py")
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    