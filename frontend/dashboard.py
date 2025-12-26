import streamlit as st
from utils.session import is_logged_in, logout_user
from frontend.upload import upload_page


def dashboard_page():
    if not is_logged_in():
        st.error("You must be logged in to access the dashboard.")
        return

    st.title("Dashboard")

    st.write(f"Welcome, **{st.session_state.user_name}** 👋")
    st.write(f"Email: {st.session_state.user_email}")
    st.write(f"Role: {st.session_state.user_role}")

    st.divider()

    st.subheader("Quick Actions")

    if st.button("Upload Book"):
        st.session_state["current_page"] = "upload"


    st.divider()

    if st.button("Logout"):
        logout_user()

    if st.session_state.get("current_page") == "upload":
        upload_page()