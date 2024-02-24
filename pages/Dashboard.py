import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import plotly.express as px
import streamlit_authenticator as stauth

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
    st.write(f'Welcome to your archery dashboard *{st.session_state["name"]}*!')
    
    
    

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
    total_sum = sum_per_column.sum()

    st.metric(label='Total Sum', value=total_sum)

    # --- KPI - Total Arrows Shot During This Week
    arrows_columns = afstanden.columns[1:]  # Exclude 'Date' column
    data['Total Arrows'] = afstanden[arrows_columns].sum(axis=1)

    # Convert 'Date' to datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Filter data for the current week
    current_week_data = data[data['Date'].dt.isocalendar().week == data['Date'].max().isocalendar().week]

    # Calculate the sum of arrows for the current week
    arrows_this_week_sum = current_week_data['Total Arrows'].sum()

    st.metric(label='Total Arrows Shot this Week', value=arrows_this_week_sum)
    
    # TODO st.metric(label="Temperature", value="70 °F", delta="1.2 °F") (aantal vorige week en nu verschil weergeven)
    
    # --- KPI - total arrows range
    
    
    #TODO
    
    
    
    # Create a 2x2 layout for the duration metrics
    col1, col2 = st.columns(2)
    
    # --- KPI - total cardio this week
    
    cardio = data[['Date','Cardio hh:mm']]
    
    # Convert 'Date' to datetime
    cardio['Date'] = pd.to_datetime(cardio['Date'])
    cardio['Cardio hh:mm'] = pd.to_timedelta(cardio['Cardio hh:mm'])
    
    # Extract week information from the date column
    cardio['week'] = cardio['Date'].dt.isocalendar().week
    
    # Sum the time spent per week
    total_time_cardio_per_week = cardio.groupby('week')['Cardio hh:mm'].sum()
    
    # Convert timedelta to hours and minutes
    total_time_per_week_hours = total_time_cardio_per_week.dt.total_seconds() / 3600
    total_time_per_week_str = total_time_per_week_hours.apply(lambda x: f"{int(x)}h {int((x % 1) * 60)}m")

    # Display the result using st.metric
    col1.metric(label='Total Time Cardio per Week', value=total_time_per_week_str.sum())
    

    # --- KPI - total gym this week 
    
    gym = data[['Date','Gym hh:mm']]
    
    # Convert 'Date' to datetime
    gym['Date'] = pd.to_datetime(gym['Date'])
    gym['Gym hh:mm'] = pd.to_timedelta(gym['Gym hh:mm'])
    
    # Extract week information from the date column
    gym['week'] = gym['Date'].dt.isocalendar().week
    
    # Sum the time spent per week
    total_time_gym_per_week = gym.groupby('week')['Gym hh:mm'].sum()
    
    # Convert timedelta to hours and minutes
    total_time_per_week_hours = total_time_gym_per_week.dt.total_seconds() / 3600
    total_time_per_week_str = total_time_per_week_hours.apply(lambda x: f"{int(x)}h {int((x % 1) * 60)}m")

    # Display the result using st.metric
    col1.metric(label='Total Time Gym per Week', value=total_time_per_week_str.sum())
    
    # --- KPI - total static this week
    
    static = data[['Date','Static Work hh:mm']]
    
    # Convert 'Date' to datetime
    static['Date'] = pd.to_datetime(static['Date'])
    static['Static Work hh:mm'] = pd.to_timedelta(static['Static Work hh:mm'])
    
    # Extract week information from the date column
    static['week'] = static['Date'].dt.isocalendar().week
    
    # Sum the time spent per week
    total_time_static_per_week = static.groupby('week')['Static Work hh:mm'].sum()
    
    # Convert timedelta to hours and minutes
    total_time_per_week_hours = total_time_static_per_week.dt.total_seconds() / 3600
    total_time_per_week_str = total_time_per_week_hours.apply(lambda x: f"{int(x)}h {int((x % 1) * 60)}m")

    # Display the result using st.metric
    col2.metric(label='Total Static Work per Week', value=total_time_per_week_str.sum())
    
    # --- KPI - total yoga this week
    
    yoga = data[['Date','Yoga hh:mm']]
    
    # Convert 'Date' to datetime
    yoga['Date'] = pd.to_datetime(yoga['Date'])
    yoga['Yoga hh:mm'] = pd.to_timedelta(yoga['Yoga hh:mm'])
    
    # Extract week information from the date column
    yoga['week'] = yoga['Date'].dt.isocalendar().week
    
    # Sum the time spent per week
    total_time_yoga_per_week = yoga.groupby('week')['Yoga hh:mm'].sum()
    
    # Convert timedelta to hours and minutes
    total_time_per_week_hours = total_time_yoga_per_week.dt.total_seconds() / 3600
    total_time_per_week_str = total_time_per_week_hours.apply(lambda x: f"{int(x)}h {int((x % 1) * 60)}m")

    # Display the result using st.metric
    col2.metric(label='Total Yoga per Week', value=total_time_per_week_str.sum())
    
    
    # TODO chart number of arrows per month/year,... plotlly interactive
    
    
    # --- PLOT
    
    # Convert 'Date' to datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Melt the DataFrame to have a 'Distance' column and a 'Value' column
    melted_data = pd.melt(data, id_vars=['Date'], var_name='Distance', value_name='Value')

    # Create a stacked bar chart
    fig = px.bar(melted_data, x='Date', y='Value', color='Distance',
                title='Arrows Shot per Day for Each Distance',
                labels={'Value': 'Arrows Shot', 'Distance': 'Distance'},
                category_orders={'Distance': sorted(data.columns[1:])})

    # Show the legend
    fig.update_layout(showlegend=True)

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)