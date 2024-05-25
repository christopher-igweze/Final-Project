from pages import st
# from Frontend.app import page

def main_page():
    st.title("Main Page")
    st.write("This is the main page of the Streamlit app.")
    st.write(f"[Go to Page 1](?page=page1)")
    st.write(f"[Go to Page 2](?page=page2)")