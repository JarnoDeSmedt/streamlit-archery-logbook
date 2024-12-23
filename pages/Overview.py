import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import streamlit_authenticator as stauth

# --- user authentication
if not st.session_state['authentication_status']:
    st.stop()  # Do not continue if check_password is not True.

# establish a google sheets connection
conn2 = st.connection("gsheets", type=GSheetsConnection)
# fetch existing data 
existing_data = conn2.read(worksheet="input_data",ttl="1m", usecols=list(range(22)))

existing_data = existing_data.dropna(how="all")

# display the dataframe
st.dataframe(existing_data)