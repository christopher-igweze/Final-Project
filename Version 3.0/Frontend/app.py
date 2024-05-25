import streamlit as st

def index_page():
    st.title("Welcome to My App")
    st.image("C:/Users/USER/Pictures/Saved Pictures/uk_pic.jpg")  # Replace with your image path
    if st.button("Login"):
        st.switch_page("pages/login.py")

if __name__ == "__main__":
    index_page()