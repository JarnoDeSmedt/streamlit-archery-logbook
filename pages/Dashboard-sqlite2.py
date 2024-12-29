import os
import sqlite3
import pandas as pd
import logging

import streamlit as st
import altair as alt
from pipelines.match_pipeline import process_match_table

from azure.storage.blob import BlobServiceClient, BlobClient

st.title('Dashboard van sqlite database')

# --- user authentication
if not st.session_state['authentication_status']:
    st.stop()  # Do not continue if check_password is not True.

# logfile aanmaken
logging.basicConfig(level=logging.INFO, filename="azureDBlogs.txt", filemode="a", format="%(asctime)s %(message)s")

# Download jarno.db from the storage account
connection_string = "DefaultEndpointsProtocol=https;AccountName=datalakearchery;AccountKey=xAa+gCRWs4JyBP/EDJcooEaw07A5GfKXTszAwgsAltUI7Ohcp+3jtwANYPBm2cy8+STAI+EDDYiv+AStAy2OqA==;EndpointSuffix=core.windows.net"
blob = BlobClient.from_connection_string(conn_str=connection_string, container_name="artemisdata", blob_name="backups-jarno/jarno.db")
jarno_db_path = "./DATA/jarno.db"
with open(jarno_db_path, "wb") as my_blob:
    blob_data = blob.download_blob().readall()
    my_blob.write(blob_data)
    print("jarno.db database downloaded!")
    logging.info("jarno.db database downloaded!\n")

# List files in the DATA directory
data_dir = './DATA'
files = [f for f in os.listdir(data_dir) if f.endswith('.db') and os.path.isfile(os.path.join(data_dir, f))]

# Add jarno.db to the list of files if not already present
if 'jarno.db' not in files:
    files.append('jarno.db')

# Streamlit dropdown to select a file, prefilled with jarno.db
selected_file = st.selectbox("Choose a database file", files, index=files.index('jarno.db'))

if selected_file:
    databasename = os.path.join(data_dir, selected_file)

    ### --- CLEANING
    # 1. match table
    conn = sqlite3.connect(databasename)
    df_match = pd.read_sql_query("SELECT * FROM match", conn)
    conn.close()
    processed_df_match = process_match_table(df_match)
    logging.info("match table cleaned!\n")

    # 2. ... table
    # conn = sqlite3.connect(databasename)
    # df_... = pd.read_sql_query("SELECT * FROM ...", conn)
    # conn.close()
    # processed_df_... = process_..._table(df_...)
    # logging.info("... cleaned!\n")


    # 3. ... table

    ### mergen van de tabellen
    # data = pd.merge(processed_df_match, processed_df_..., how='left', on='...')







### --- VISUALISATION
## Overview Section
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
conn = sqlite3.connect(databasename)
overview = pd.read_sql_query(overview_query, conn)
st.metric("Total Matches", overview["total_matches"].iloc[0])
st.metric("Total Sessions", overview["total_sessions"].iloc[0])
st.metric("Total Shots", overview["total_shots"].iloc[0])


# KPI: total cardio this week

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

# KPI: total gym this week

# KPI: total arrows this week (so far) 

# KPI: weekly average of arrows

# KPI: average arrows per day

# KPI: pi chart ratio distances shot

# KPI: pi chart ratio of alternative trinings like gym, yoga, cardio or static

# TODO: decide what do you want to see? 






# chart: interactive chart of total arrows per day, week, month, year

# chart: interactive chart of scores (possible to combine with the above chart, to show it on top in a line chart?)

# plot: arrowplot section


## Scoring section

# table season performance training - competition with grouping artemis

# match play performance


## Raw data section (maybe let this out...)

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


