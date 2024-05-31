import streamlit as st
from utils import load_css, page_config
import yaml, os
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import time

page_config()
load_css()

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
    st.switch_page("pages/db.py")
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    

def forgot_password():
    # Creating a forgot password widget
    try:
        username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password(clear_on_submit=True)
        if username_of_forgotten_password:
            # st.success('New password to be sent securely')
            with open(path, 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
            # i'll set up an email system later
            container = st.empty()
            container.success(f"Here's the new password: {new_random_password}")  # Create a success alert
            time.sleep(6)  # Wait 6 seconds
            container.empty()
            # The developer should securely transfer the new password to the user.
        elif username_of_forgotten_password == False:
            st.error('Username not found')
    except Exception as e:
        st.error(e)

def forgot_username():
    # Creating a forgot username widget
    try:
        username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username(clear_on_submit=True)
        if username_of_forgotten_username:
            # st.success('Username to be sent securely')
            with open(path, 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
            # i'll set up an email system later
            container = st.empty()
            container.success(f"Here's your username: {username_of_forgotten_username}")  # Create a success alert
            time.sleep(6)  # Wait 2 seconds
            container.empty()
            # The developer should securely transfer the username to the user.
        elif username_of_forgotten_username == False:
            st.error('Email not found')
    except Exception as e:
        st.error(e)

user = False
passd = False
col1, col2 = st.columns([0.15, 0.85])

with col1:
    if st.button("Forgot Username"):
        user = True
        passd = False

with col2:
    if st.button("Forgot Password"):
        user = False
        passd = True


if user == True:
    forgot_username()
if passd == True:
    forgot_password()

# make it a pop up form