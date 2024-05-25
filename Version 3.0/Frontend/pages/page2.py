from pages import st

def page1():
    st.title("Page 1")
    st.write("This is the first additional page.")
    st.write(f"[Go to Main Page](?page=main)")
    st.write(f"[Go to Page 2](?page=page2)")