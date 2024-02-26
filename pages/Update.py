import streamlit as st
import streamlit_authenticator as stauth
from streamlit_gsheets import GSheetsConnection
import pandas as pd

import datetime

# --- user authentication
import yaml
from yaml.loader import SafeLoader
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login(location='main')

if st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
    st.title("Update records")

    # Establish a Google Sheets connection
    conn4 = st.connection("gsheets", type=GSheetsConnection)

    # Fetch existing data
    existing_data = conn4.read(worksheet="input_data",ttl="1m", usecols=list(range(22)))
    existing_data = existing_data.dropna(how="all")

    # Date to update
    date_to_update = st.date_input(label="Select date to update")

    # Function to fetch existing data for the selected date
    def fetch_existing_data_for_date(date_to_update, existing_data):
        return existing_data[existing_data['Date'] == date_to_update.strftime("%Y-%m-%d")]

    # Fetch existing data for the selected date
    existing_data_for_date = fetch_existing_data_for_date(date_to_update, existing_data)

    # Update entry form
    with st.form(key="update_form", clear_on_submit=True):
        # If data exists for the selected date, populate the form with existing data
        if not existing_data_for_date.empty:
            st.write("Existing data found. Update the details.")
            date = st.date_input(label="Date*", value=pd.to_datetime(existing_data_for_date['Date']).dt.date.iloc[0])
            time_shooting = st.time_input(
                label="Shooting time",
                value=datetime.datetime.strptime(existing_data_for_date['Time hh:mm'].iloc[0], "%H:%M:%S").time()
            )
            blank_bale = st.number_input(label="Blank bale", value=existing_data_for_date['Blank 5m'].iloc[0])
            m18 = st.number_input(label="18m", value=existing_data_for_date['18m'].iloc[0])
            m25 = st.number_input(label="25m", value=existing_data_for_date['25m'].iloc[0])
            m30 = st.number_input(label="30m", value=existing_data_for_date['30m'].iloc[0])
            m35 = st.number_input(label="35m", value=existing_data_for_date['35m'].iloc[0])
            m40 = st.number_input(label="40m", value=existing_data_for_date['40m'].iloc[0])
            m45 = st.number_input(label="45m", value=existing_data_for_date['45m'].iloc[0])
            m50 = st.number_input(label="50m", value=existing_data_for_date['50m'].iloc[0])
            m55 = st.number_input(label="55m", value=existing_data_for_date['55m'].iloc[0])
            m60 = st.number_input(label="60m", value=existing_data_for_date['60m'].iloc[0])
            m70 = st.number_input(label="70m", value=existing_data_for_date['70m'].iloc[0])
            m80 = st.number_input(label="80m", value=existing_data_for_date['80m'].iloc[0])
            m90 = st.number_input(label="90m", value=existing_data_for_date['90m'].iloc[0])
            arrows_comp = st.number_input(label="Arrows shot_comp", value=existing_data_for_date['Arrows shot_comp'].iloc[0])
            field = st.number_input(label="Field", value=existing_data_for_date['Field'].iloc[0])
            cardio_time = st.time_input(
                label="Cardio time",
                value=datetime.datetime.strptime(existing_data_for_date['Cardio hh:mm'].iloc[0], "%H:%M:%S").time()
            )
            yoga_time = st.time_input(
                label="Yoga time",
                value=datetime.datetime.strptime(existing_data_for_date['Yoga hh:mm'].iloc[0], "%H:%M:%S").time()
            )
            static_time = st.time_input(
                label="Static Work time",
                value=datetime.datetime.strptime(existing_data_for_date['Static Work hh:mm'].iloc[0], "%H:%M:%S").time()
            )
            gym_time = st.time_input(
                label="Gym time",
                value=datetime.datetime.strptime(existing_data_for_date['Gym hh:mm'].iloc[0], "%H:%M:%S").time()
            )
            comment = st.text_area(label="special comment", value=existing_data_for_date['Special commentary'].iloc[0])

            st.markdown("**required*")
            
            submit_button = st.form_submit_button(label="Update")

            if submit_button:
                st.write("You pressed Update!")
                
                # Update the existing data for the selected date
                existing_data.loc[existing_data['Date'] == date_to_update.strftime("%Y-%m-%d")] = {
                    "Date": date.strftime("%Y-%m-%d"),
                    "Time hh:mm": time_shooting,
                    "Blank 5m": blank_bale,
                    "18m": m18,
                    "25m": m25,
                    "30m": m30,
                    "35m": m35,
                    "40m": m40,
                    "45m": m45,
                    "50m": m50,
                    "55m": m55,
                    "60m": m60,
                    "70m": m70,
                    "80m": m80,
                    "90m": m90,
                    "Field": field,
                    "Arrows shot_comp": arrows_comp,
                    "Cardio hh:mm": cardio_time,
                    "Yoga hh:mm": yoga_time,
                    "Static Work hh:mm": static_time,
                    "Gym hh:mm": gym_time,
                    "Special commentary": comment
                }
                
                # Update Google Sheets
                conn4.update(worksheet="input_data", data=existing_data)
                
                st.success("Data is successfully updated!")
        else:
            st.warning("No existing data found for the selected date.")