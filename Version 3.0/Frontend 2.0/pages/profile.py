import streamlit as st
from json import load
import streamlit as st
import yaml, os
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from utils import load_css, page_config, menu

page_config()
load_css()
menu()

st.title("Profile Page")
st.write("This page is for viewing and editing your profile information.")

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

# Authenticating Users
if st.session_state["authentication_status"]:
    authenticator.logout()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.switch_page("app.py")