from ast import main
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
from urllib.parse import urlencode, parse_qs
from pages.index import main_page
from pages.page2 import page1
from pages.page3 import page2


# Main app logic
def run_app():

    # Creating a login widget
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

    authenticator.login() # to render the login form

    # Authenticating Users
    if st.session_state["authentication_status"]:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')


if __name__ == "__main__":
    run_app()

