import hmac
from pathlib import Path
import datetime
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_gsheets import GSheetsConnection
from streamlit_option_menu import option_menu
import pandas as pd

# Set the width of the entire Streamlit app page
st.set_page_config(layout="wide")

# --- user authentication
import yaml
from yaml.loader import SafeLoader
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
except Exception as e:
    if isinstance(e, stauth.streamlit.errors.StreamlitWebSocketError):
        st.warning("Connection lost. Please reload the page.")
    else:
        st.error(f"An unexpected error occurred: {e}")

if st.session_state['authentication_status']:
    authenticator.logout()
    # display title
    name = st.session_state["name"]
    st.title(f"Welcome to your archery logbook, *{name}*!")

elif st.session_state['authentication_status'] is False:
    st.error('😕 Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')

