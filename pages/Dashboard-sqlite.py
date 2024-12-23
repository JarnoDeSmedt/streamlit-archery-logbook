import streamlit as st
import os
import sqlite3
import pandas as pd
import altair as alt
import datetime
from datetime import datetime

st.title('Dashboard van sqlite database')

# --- user authentication
if not st.session_state['authentication_status']:
    st.stop()  # Do not continue if check_password is not True.

# List files in the DATA directory
data_dir = './DATA'
files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]

# Streamlit dropdown to select a file
selected_file = st.selectbox("Choose a database file", files)

if selected_file:
    databasename = os.path.join(data_dir, selected_file)

conn = sqlite3.connect(databasename)

# Overview Section
st.header("Overview")
overview_query = """
    SELECT 
        COUNT(DISTINCT m._id) AS total_matches,
        COUNT(DISTINCT k._id) AS total_sessions,
        COUNT(s._id) AS total_shots
    FROM match m
    LEFT JOIN kuiperslist k ON k.date = m.date
    LEFT JOIN shot s ON s.match_id = m._id
"""
overview = pd.read_sql_query(overview_query, conn)
st.metric("Total Matches", overview["total_matches"].iloc[0])
st.metric("Total Sessions", overview["total_sessions"].iloc[0])
st.metric("Total Shots", overview["total_shots"].iloc[0])



# TODO: decide what do you want to see? 





# --- Show KPIs

# --- KPI - total cardio this week

# cardio = data[['Date', 'Cardio hh:mm']]
# # Convert 'Date' to datetime
# cardio['Date'] = pd.to_datetime(cardio['Date'])
# cardio['Cardio hh:mm'] = pd.to_timedelta(cardio['Cardio hh:mm'])
# # Extract week information from the date column
# cardio['week'] = cardio['Date'].dt.isocalendar().week
# # Sum the time spent per week
# total_time_cardio_per_week = cardio.groupby('week')['Cardio hh:mm'].sum()
# # Sum the total time in seconds
# total_seconds = total_time_cardio_per_week.dt.total_seconds().sum()
# # Convert total seconds to hours and minutes
# total_hours = int(total_seconds / 3600)
# total_minutes = int((total_seconds % 3600) / 60)
# # Format the total time as a string
# total_time_str = f"{total_hours}h {total_minutes}m"

# # Display the result using st.metric
# st.metric(label='Total Time Cardio per Week', value=total_time_str)




# --- Show the data
st.markdown('---')
c = conn.cursor()
c.execute('SELECT * FROM match')
data = c.fetchall()
conn.close()

# Convert the data to a pandas DataFrame
data = pd.DataFrame(data)

with st.expander("Show table"):
    st.write(data)


