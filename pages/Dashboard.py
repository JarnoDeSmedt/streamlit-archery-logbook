import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

if st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
    st.write(f'Welcome to your archery dashboard *{st.session_state["name"]}*!')



    # basic dashboard hours trained per month, arrows shot last week, month,...

