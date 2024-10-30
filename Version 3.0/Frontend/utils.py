import streamlit as st
from json import load
import streamlit as st
import yaml, os
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import smtplib

path = os.path.join(os.path.dirname(__file__), 'config.yaml')

with open(path) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

def load_css():
    with open("assets/styles/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def menu():
    st.sidebar.image("assets/images/cu2.png", width=200, use_column_width=True)
    st.sidebar.page_link("app.py", label="🏡 Home")
    st.sidebar.page_link("pages/db.py", label="📂 Program Data")
    st.sidebar.page_link("pages/createTT.py", label="🔨 Create Timetable")
    st.sidebar.page_link("pages/viewTT.py", label="📄 View Timetable")
    st.sidebar.page_link("pages/constraints.py", label="🔒 Constraints")
    st.sidebar.page_link("pages/profile.py", label="🧙🏼‍♂️ Profile")
    # st.sidebar.markdown("---")
    # if st.sidebar.button("Logout", key="logoutbutton", type="secondary"):
    #     authenticator.logout()
    #     st.switch_page("app.py")

def guestMenu():
    st.sidebar.image("assets/images/cu2.png", width=200, use_column_width=True)
    st.sidebar.page_link("app.py", label="👈🏼 Logout")
    # st.sidebar.page_link("pages/db.py", label="📂 Database")
    # st.sidebar.page_link("pages/createTT.py", label="🔨 Create Timetable")
    st.sidebar.page_link("pages/viewTT.py", label="📄 View Timetable")
    # st.sidebar.page_link("pages/constraints.py", label="🔒 Constraints")
    # st.sidebar.page_link("pages/profile.py", label="🧙🏼‍♂️ Profile")
    # st.sidebar.markdown("---")
    # if st.sidebar.button("Logout", key="logoutbutton", type="secondary"):
    #     authenticator.logout()
    #     st.switch_page("app.py")

def email(email, password, value):
    HOST = "smtp-mail.outlook.com"
    PORT = 587

    FROM_EMAIL = "christopher.igweze@outlook.com"
    TO_EMAIL = email
    PASSWORD = "od04QWgwu.123"


    MESSAGE_PASS = f"""Subject: Password Recovery

    Here is your new password: {password}

    Keep it safe, do not show anybody. Have a nice day.
    
    
    Igweze Ifeanyi, Covenant University Timetable Officer."""

    MESSAGE_NAME = f"""Subject: Password Recovery

    Here is your username: {password}

    Keep it safe, do not show anybody. Have a nice day.
    
  
    Igweze Ifeanyi, Covenant University Timetable Officer."""

    if value == True: MESSAGE = MESSAGE_PASS 
    else: MESSAGE = MESSAGE_NAME 

    smtp = smtplib.SMTP(HOST, PORT)

    status_code, response = smtp.ehlo()
    print(f"[*] Echoing the server: {status_code} {response}")

    status_code, response = smtp.starttls()
    print(f"[*] Echoing the server: {status_code} {response}")

    status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
    print(f"[*] Echoing the server: {status_code} {response}")

    smtp.sendmail(FROM_EMAIL, TO_EMAIL, MESSAGE)
    smtp.quit()