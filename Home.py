import pickle
from pathlib import Path
import datetime

import streamlit as st
import streamlit_authenticator as stauth
from streamlit_gsheets import GSheetsConnection
from streamlit_option_menu import option_menu

# for speak button
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events


import pandas as pd

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


if authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
elif authentication_status:
    authenticator.logout('Logout', 'main')

    
    # display title
    st.title(f"Welcome to your archery logbook {name}!")

    # --- button to speak
    #AI_button = st.button(label="Quick way [microfoon]")
    stt_button = Button(label="Speak", width=100)

    stt_button.js_on_event("button_click", CustomJS(code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = function (e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if ( value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        }
        recognition.start();
        """))

    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0)

    if result:
        if "GET_TEXT" in result:
            st.write(result.get("GET_TEXT"))

    # ---

    st.markdown("Enter the details of your training session below")


    # establish a google sheets connection
    conn = st.connection("gsheets", type=GSheetsConnection )

    # fetch existing data 
    existing_data = conn.read(worksheet="input_data", usecols=list(range(22)))

    existing_data = existing_data.dropna(how="all")

    # display the dataframe
    #st.dataframe(existing_data)

    # list of types

    TYPES = [
        "type1",
        "type2",
        "type3"
    ]


    # new entry form
    with st.form(key="entry_form", clear_on_submit=True):
        date = st.date_input(label="date*")
        time_shooting = st.time_input(label="shooting time", value= datetime.time(0, 00))
        blank_bale = st.number_input(label="blank bale", step = 1, value=None)
        m18 = st.number_input(label="18m", step = 1, value=None)
        m25 = st.number_input(label="25m", step = 1, value=None)
        m30 = st.number_input(label="30m", step = 1, value=None)
        m35 = st.number_input(label="35m", step = 1, value=None)
        m40 = st.number_input(label="40m", step = 1, value=None)
        m45 = st.number_input(label="45m", step = 1, value=None)
        m50 = st.number_input(label="50m", step = 1, value=None)
        m55 = st.number_input(label="55m", step = 1, value=None)
        m60 = st.number_input(label="60m", step = 1, value=None)
        m70 = st.number_input(label="70m", step = 1, value=None)
        m80 = st.number_input(label="80m", step = 1, value=None)
        m90 = st.number_input(label="90m", step = 1, value=None)
        arrows_comp = st.number_input(label="Arrows shot_comp", step = 1, value=None)
        field = st.number_input(label="field", step = 1, value=None)
        cardio_time = st.time_input(label="cardio time", value= datetime.time(0, 00))
        yoga_time = st.time_input(label="yoga time", value= datetime.time(0, 00))
        static_time = st.time_input(label="static work time", value= datetime.time(0, 00))
        gym_time = st.time_input(label="gym time", value= datetime.time(0, 00))
        comment = st.text_area("special comment")
        
        st.markdown("**required*")
        
        submit_button = st.form_submit_button(label="Submit")
        
        if submit_button:
            st.write("you pressed submit!")
            
            #checks...
            # - data bestaat al
            
            input_data = pd.DataFrame(
                [
                    {
                        "Date": date.strftime("%Y-%m-%d"),
                        "Special commentary": comment,
                        "Time hh:mm": time_shooting,
                        "90m": m90,
                        "80m": m80,
                        "70m": m70,
                        "60m": m60,
                        "55m": m55,
                        "50m": m50,
                        "45m": m45,
                        "40m": m40,
                        "35m": m35,
                        "30m": m30,
                        "25m": m25,
                        "18m": m18,
                        "Blank 5m": blank_bale,
                        "Field": field,
                        "Arrows shot_comp": arrows_comp,
                        "Gym hh:mm": gym_time,
                        "Yoga hh:mm": yoga_time,
                        "Cardio hh:mm": cardio_time,
                        "Static Work hh:mm": static_time
                
                    }
                ]
            )
            
            # add new data to existing data
            updated_df = pd.concat([existing_data, input_data], ignore_index=True)
            
            # update gg sheets
            
            conn.update(worksheet="input_data", data=updated_df)
            
            st.success("data is succesfully sent!")
            
            
        

