import streamlit as st
from utils import load_css, email
import yaml, os
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import time
from user_db import update_database

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
st.image("assets/images/cu.png")
path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')

with open(path) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
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
            value = True
            email(email_of_forgotten_password, new_random_password, value)
            container = st.empty()
            container.success("New password has been sent to your email. Check your spam/junk folder")  # Create a success alert
            update_database()
            time.sleep(6)  # Wait 6 seconds
            container.empty()
            # The developer should securely transfer the new password to the user.
        elif email_of_forgotten_password == False:
            st.error('Email not found')
    except Exception as e:
        st.error(e)

def forgot_username():
    # Creating a forgot username widget
    try:
        username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username(clear_on_submit=True)
        if email_of_forgotten_username:
            # st.success('Username to be sent securely')
            with open(path, 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
            value = False
            email(email_of_forgotten_username, username_of_forgotten_username, value)
            container = st.empty()
            container.success("Your username has been sent to your email\nCheck your spam/junk folder")  # Create a success alert
            time.sleep(6)  # Wait 2 seconds
            container.empty()
            # The developer should securely transfer the username to the user.
        elif email_of_forgotten_username == False:
            st.error('Email not found')
    except Exception as e:
        st.error(e)

user = False
passd = False
col1, col2 = st.columns([0.15, 0.85])

with col1:
    with st.popover("Forgot Username"):
        forgot_username()

with col2:
    with st.popover("Forgot Password"):
        forgot_password()

if st.button('Login as Student / Lecturer'):
    st.switch_page("pages/guestViewTT.py")