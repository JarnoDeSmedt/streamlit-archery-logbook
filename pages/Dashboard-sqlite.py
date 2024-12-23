import streamlit as st

import pandas as pd
import datetime
from datetime import datetime

st.title('Dashboard van sqlite database')

# Load the data from the sqlite database
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('SELECT * FROM data')
data = c.fetchall()
conn.close()

# Convert the data to a pandas DataFrame
data = pd.DataFrame(data, columns=['Date', 'Cardio hh:mm', 'Gym hh:mm'])

# Display the data
st.write(data)

# --- KPI - total cardio this week

cardio = data[['Date', 'Cardio hh:mm']]
# Convert 'Date' to datetime
cardio['Date'] = pd.to_datetime(cardio['Date'])
cardio['Cardio hh:mm'] = pd.to_timedelta(cardio['Cardio hh:mm'])
# Extract week information from the date column
cardio['week'] = cardio['Date'].dt.isocalendar().week
# Sum the time spent per week
total_time_cardio_per_week = cardio.groupby('week')['Cardio hh:mm'].sum()
# Sum the total time in seconds
total_seconds = total_time_cardio_per_week.dt.total_seconds().sum()
# Convert total seconds to hours and minutes
total_hours = int(total_seconds / 3600)
total_minutes = int((total_seconds % 3600) / 60)
# Format the total time as a string
total_time_str = f"{total_hours}h {total_minutes}m"

# Display the result using st.metric
st.metric(label='Total Time Cardio per Week', value=total_time_str)