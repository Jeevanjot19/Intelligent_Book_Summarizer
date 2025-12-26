import streamlit as st
from frontend.auth import auth_router
from frontend.dashboard import dashboard_page
from utils.session import init_session, is_logged_in

st.set_page_config(page_title="Intelligent Book Summarizer", layout="centered")

init_session()

if is_logged_in():
    dashboard_page()
else:
    auth_router()
