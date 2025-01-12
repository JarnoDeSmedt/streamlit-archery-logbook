import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
from datetime import datetime
import plotly.express as px
import streamlit_authenticator as stauth

# --- user authentication
if not st.session_state['authentication_status']:
    st.stop()  # Do not continue if check_password is not True.


    
st.markdown("---")

# Create a 2x2 layout for the duration metrics
col1, col2 = st.columns(2)


# establish a google sheets connection
conn3 = st.connection("gsheets", type=GSheetsConnection)
# fetch existing data 
data = conn3.read(worksheet="input_data", usecols=list(range(22)))
data = data.dropna(how="all")

afstanden = data[['Date','90m','80m','70m','60m','55m','50m','45m','40m','35m','30m','25m','18m','Blank 5m', 'Field', 'Arrows shot_comp']]



# --- KPI - total arrows (fun)
# Calculate total sum across columns
afstanden_num = afstanden.apply(pd.to_numeric, errors='coerce')
sum_per_column = afstanden_num.sum(axis=0)
total_sum = int(sum_per_column.sum())

col2.metric(label='Total Sum', value=total_sum)

# --- KPI - Total Arrows Shot During This Week
arrows_columns = afstanden.columns[1:]  # Exclude 'Date' column
data['Total Arrows'] = afstanden[arrows_columns].sum(axis=1)

# Convert 'Date' to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Filter data for the current week
current_week_data = data[data['Date'].dt.isocalendar().week == data['Date'].max().isocalendar().week]

# Calculate the sum of arrows for the current week
arrows_this_week_sum = int(current_week_data['Total Arrows'].sum())

col1.metric(label='Total Arrows Shot this Week', value=arrows_this_week_sum)

# TODO st.metric(label="Temperature", value="70 °F", delta="1.2 °F") (aantal vorige week en nu verschil weergeven)



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
col1.metric(label='Total Time Cardio per Week', value=total_time_str)



# --- KPI - total gym this week 

gym = data[['Date', 'Gym hh:mm']]

# Convert 'Date' to datetime
gym['Date'] = pd.to_datetime(gym['Date'])
gym['Gym hh:mm'] = pd.to_timedelta(gym['Gym hh:mm'])

# Extract week information from the date column
gym['week'] = gym['Date'].dt.isocalendar().week

# Sum the time spent per week
total_time_gym_per_week = gym.groupby('week')['Gym hh:mm'].sum()

# Sum the total time in seconds
total_seconds_gym = total_time_gym_per_week.dt.total_seconds().sum()

# Convert total seconds to hours and minutes
total_hours_gym = int(total_seconds_gym / 3600)
total_minutes_gym = int((total_seconds_gym % 3600) / 60)

# Format the total time as a string
total_time_str_gym = f"{total_hours_gym}h {total_minutes_gym}m"

# Display the result using st.metric
col1.metric(label='Total Time Gym per Week', value=total_time_str_gym)  ###


# --- KPI - total static this week

static = data[['Date', 'Static Work hh:mm']]

# Convert 'Date' to datetime
static['Date'] = pd.to_datetime(static['Date'])
static['Static Work hh:mm'] = pd.to_timedelta(static['Static Work hh:mm'])

# Extract week information from the date column
static['week'] = static['Date'].dt.isocalendar().week

# Sum the time spent per week
total_time_static_per_week = static.groupby('week')['Static Work hh:mm'].sum()

# Sum the total time in seconds
total_seconds_static = total_time_static_per_week.dt.total_seconds().sum()

# Convert total seconds to hours and minutes
total_hours_static = int(total_seconds_static / 3600)
total_minutes_static = int((total_seconds_static % 3600) / 60)

# Format the total time as a string
total_time_str_static = f"{total_hours_static}h {total_minutes_static}m"

# Display the result using st.metric
col2.metric(label='Total Static Work per Week', value=total_time_str_static)  ###


# --- KPI - total yoga this week

yoga = data[['Date', 'Yoga hh:mm']]

# Convert 'Date' to datetime
yoga['Date'] = pd.to_datetime(yoga['Date'])
yoga['Yoga hh:mm'] = pd.to_timedelta(yoga['Yoga hh:mm'])

# Extract week information from the date column
yoga['week'] = yoga['Date'].dt.isocalendar().week

# Sum the time spent per week
total_time_yoga_per_week = yoga.groupby('week')['Yoga hh:mm'].sum()

# Sum the total time in seconds
total_seconds_yoga = total_time_yoga_per_week.dt.total_seconds().sum()

# Convert total seconds to hours and minutes
total_hours_yoga = int(total_seconds_yoga / 3600)
total_minutes_yoga = int((total_seconds_yoga % 3600) / 60)

# Format the total time as a string
total_time_str_yoga = f"{total_hours_yoga}h {total_minutes_yoga}m"

# Display the result using st.metric
col2.metric(label='Total Yoga per Week', value=total_time_str_yoga)  ###


st.markdown("""---""")

st.subheader("Periodical Summary")

st.write("Make selections in the left sidebar to update")

# --- KPI - total arrows range

# Add a date range picker for date selection
st.sidebar.subheader('Select Date Range')

# Convert start and end dates to Timestamps
start_date = pd.to_datetime(st.sidebar.date_input('Start Date', data['Date'].min()))
end_date = pd.to_datetime(st.sidebar.date_input('End Date', data['Date'].max()))

# Convert 'Date' column to Timestamps
data['Date'] = pd.to_datetime(data['Date'])

# Filter data based on selected date range
filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

# Display the total arrows metric for the selected date range
total_arrows_for_selected_range = int(filtered_data['Total Arrows'].sum())
st.metric(label='Total Arrows from date range', value=total_arrows_for_selected_range)


# TODO chart number of arrows per week/month/year,... plotlly interactive

# TODO metric of 100% week 
# TODO chart pe

# --- PLOT
st.write("Arrows Shot per Day for Each Distance")

# Simplify data preparation
arrowplotdata = data.copy()
arrowplotdata['Date'] = pd.to_datetime(arrowplotdata['Date'])
# Drop unnecessary columns
arrowplotdata.drop(columns=['Time hh:mm', 'Special commentary', 'Gym hh:mm', 'Yoga hh:mm','Cardio hh:mm', 'Static Work hh:mm'], inplace=True)

# Melt the DataFrame to have 'Distance' and 'Value'
melted_data = pd.melt(arrowplotdata, id_vars=['Date'], var_name='Distance', value_name='Value')
melted_data = melted_data[melted_data['Distance'] != 'Total Arrows']

# Create the plot with all data
fig = px.bar(melted_data, x='Date', y='Value', color='Distance',
            labels={'Value': 'Arrows Shot', 'Distance': 'Distance'},
            category_orders={'Distance': sorted(data.columns[1:])})

# Layout adjustments for readability
fig.update_layout(
    width=1200,
    height=700,
    margin=dict(t=100),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=20)),
    dragmode='pan'  # Allow panning
)

# Dynamically determine the range to focus on the current month
first_day_of_current_month = datetime.now().replace(day=1)
last_day_of_current_month = datetime.now()

# Adjust x-axis to focus on the current month by default
fig.update_xaxes(
    rangeslider_visible=True,
    range=[first_day_of_current_month, last_day_of_current_month]
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)
