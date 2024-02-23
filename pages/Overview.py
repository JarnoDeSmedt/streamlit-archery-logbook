import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

if st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
    st.write(f"*{st.session_state['name']}*'s overview")


    # establish a google sheets connection
    conn2 = st.connection("gsheets", type=GSheetsConnection)
    # fetch existing data 
    existing_data = conn2.read(worksheet="input_data", usecols=list(range(22)))

    existing_data = existing_data.dropna(how="all")

    # display the dataframe
    st.dataframe(existing_data)