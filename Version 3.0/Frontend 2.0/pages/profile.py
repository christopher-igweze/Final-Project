import streamlit as st
from json import load
import streamlit as st
import yaml, os
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
from utils import load_css, menu
import time

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

# time the success messages of the other widgets to disappear

# Creating a reset password widget
if st.session_state["authentication_status"]:
    try:
        if authenticator.reset_password(st.session_state["username"], clear_on_submit=True):
            st.success('Password modified successfully')
            with open(path, 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)


# Creating a new baby user registration widget
try:
    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(clear_on_submit=True, pre_authorization=False)
    if email_of_registered_user:
        st.success('User registered successfully')
        with open(path, 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
except Exception as e:
    st.error(e)


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
        time.sleep(6)  # Wait 6 seconds
        container.empty()
        # The developer should securely transfer the username to the user.
    elif username_of_forgotten_username == False:
        st.error('Email not found')
except Exception as e:
    st.error(e)

# Creating an update user details widget
if st.session_state["authentication_status"]:
    try:
        if authenticator.update_user_details(st.session_state["username"], clear_on_submit=True):
            st.success('Entries updated successfully')
            with open(path, 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)