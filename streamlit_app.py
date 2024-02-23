import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# display title and description

st.title('data entry form')
st.markdown("enter the details of training below")


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
with st.form(key="entry_form"):
    date = st.date_input(label="date*")
    time_shooting = st.time_input(label="shooting time")
    blank_bale = st.number_input(label="blank bale")
    m18 = st.number_input(label="18m")
    m25 = st.number_input(label="25m")
    m30 = st.number_input(label="30m")
    m35 = st.number_input(label="35m")
    m40 = st.number_input(label="40m")
    m45 = st.number_input(label="45m")
    m50 = st.number_input(label="50m")
    m55 = st.number_input(label="55m")
    m60 = st.number_input(label="60m")
    m70 = st.number_input(label="70m")
    m80 = st.number_input(label="80m")
    m90 = st.number_input(label="90m")
    arrows_comp = st.number_input(label="Arrows shot_comp")
    field = st.number_input(label="field")
    cardio_time = st.time_input(label="cardio time")
    yoga_time = st.time_input(label="yoga time")
    static_time = st.time_input(label="static work time")
    gym_time = st.time_input(label="gym time")
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
        
        
    

