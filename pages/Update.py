import streamlit as st

if st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
    st.title("Update records")

    date_to_update = st.date_input(label="date to update")

    st.write(date_to_update)
