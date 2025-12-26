import streamlit as st


def init_session():
    """
    Initialize session state variables if not present.
    """
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None

def login_user_session(user):
    """
    Populate session state after successful login.
    """
    st.session_state.logged_in = True
    st.session_state.user_id = user["user_id"]
    st.session_state.user_name = user["name"]
    st.session_state.user_email = user["email"]
    st.session_state.user_role = user["role"]

def logout_user():
    """
    Clear session state on logout.
    """
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.session_state.logged_in = False
    st.rerun()


def is_logged_in():
    return st.session_state.get("logged_in", False)