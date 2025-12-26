import re
import streamlit as st
from backend.auth import register_user,login_user
from utils.session import login_user_session

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def is_valid_email(email: str) -> bool:
    return re.match(EMAIL_REGEX, email) is not None

def is_valid_password(password: str) -> bool:
    """
    Password rules:
    - At least 8 characters
    - At least one uppercase
    - At least one lowercase
    - At least one digit
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True

def register_page():
    st.subheader("Create an Account")

    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submit = st.form_submit_button("Register")

    if submit:
        # Frontend validation
        if not name.strip():
            st.error("Name cannot be empty.")
            return

        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return

        if not is_valid_password(password):
            st.error(
                "Password must be at least 8 characters long and contain "
                "uppercase, lowercase, and a number."
            )
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        # Call backend
        result = register_user(name, email, password)

        if result["success"]:
            st.success(result["message"])
            st.info("You can now log in.")
        else:
            st.error(result["message"])

def login_page():
    st.subheader("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submit = st.form_submit_button("Login")

    if submit:
        if not email or not password:
            st.error("Please enter both email and password.")
            return

        result = login_user(email, password)

        if not result["success"]:
            st.error(result["message"])
            return

        # Set session using helper
        login_user_session(result["user"])

        st.success("Login successful!")
        st.rerun()


def auth_router():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        st.success(f"Welcome, {st.session_state['user_name']}!")
        return

    page = st.radio("Select an option", ["Login", "Register"])

    if page == "Login":
        login_page()
    else:
        register_page()