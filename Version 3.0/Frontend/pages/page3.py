from pages import st

def page2():
    st.title("Page 2")
    st.write("This is the second additional page.")
    st.write(f"[Go to Main Page](?page=main)")
    st.write(f"[Go to Page 1](?page=page1)")