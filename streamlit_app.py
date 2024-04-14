#%%
from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from annotated_text import annotated_text
from datetime import datetime, timedelta
import calendar
import datetime
from requests import request
import altair as alt

"""
# Weather App!

"""
annotated_text(("Erick Vega", "author"))

st.header("Instructions")
st.write("1. Enter your OpenWeatherMap API key in the sidebar.")
st.write("2. Select a month from the dropdown.")
st.write("3. Use the slider to select a temperature. (This will be used to determine the number of hours the temperature was above the user input value.)")
st.write("4. Click the 'Submit' button to generate the weather data for all BYU locations.")

st.header("Results")


byu_locations = {"BYU Idaho": {"lat": 43.825386, "lon": -111.792824},
                 "BYU Provo": {"lat":  40.233845, "lon": -111.658531},
                 "BYU Hawaii": {"lat": 21.648287, "lon": -157.922562}
                 }

months = {
    "October 2023": {"month": 10, "year": 2023},
    "November 2023": {"month": 11, "year": 2023},
    "December 2023": {"month": 12, "year": 2023},
    "January 2024" : {"month": 1, "year": 2024},
    "February 2024" : {"month": 2, "year": 2024},
    "March 2024" : {"month": 3, "year": 2024},
    }

def reset_submit_clicked():
    if 'submit_clicked' not in st.session_state:
        st.session_state['submit_clicked'] = False

    if 'all_cities' not in st.session_state:
        st.session_state['all_cities'] = False
    
    st.session_state['submit_clicked'] = False
    st.session_state['all_cities'] = False

## USER INPUTS
api_key = st.sidebar.text_input("API Key:")
month_user = st.sidebar.selectbox("Month:", list(months.keys()), index=0, on_change=reset_submit_clicked)
user_temp = st.sidebar.slider("User Temp:", 0, 100, 45)

if 'submit_clicked' not in st.session_state:
    st.session_state['submit_clicked'] = False

if st.sidebar.button('Submit') or st.session_state['submit_clicked']:
    st.session_state['submit_clicked'] = True

    st.write("Please Wait...")

    year = months[month_user]["year"]
    month = months[month_user]["month"]
    _, last_day = calendar.monthrange(year, month)


    # GET WEATHER DATA FOR ALL CITIES
    if 'all_cities' not in st.session_state:
        st.session_state['all_cities'] = False

    if not st.session_state['all_cities']:    
        all_cities = {}

        for city, location in byu_locations.items():
            lat = location["lat"]
            lon = location["lon"]

            start = datetime.datetime(year, month, 1, 0, 0, 0, tzinfo=datetime.timezone.utc).timestamp()
            print(f"Start: {year}-{month}-01 01:00:00")

            end = datetime.datetime(year, month, last_day, 23, 59, 59, tzinfo=datetime.timezone.utc).timestamp()
            print(f"End: {year}-{month}-{last_day} 23:59:59")

            if lat and lon and start and end and api_key:
                while start <= end:
                    api_url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={int(start)}&end={int(end)}&units=imperial&appid={api_key}"
                    print(f"api_url : {api_url}")
                    data = request("get", api_url).json()

                    if city not in all_cities:
                        all_cities[city] = data['list']
                    else:
                        all_cities[city] = all_cities[city] + data['list']

                    last_dt = data['list'][-1]['dt']
                    start = datetime.datetime.fromtimestamp(last_dt, tz=datetime.timezone.utc).timestamp() + 3600

            else:
                print("Missing information to make the request")

        st.session_state['all_cities'] = all_cities
    
    else:
        all_cities = st.session_state['all_cities']


    # EXTRACT RELEVANT DATA
    monthly_data = {}

    for city, data in all_cities.items():
        for observation in data:

            date = datetime.datetime.fromtimestamp(observation["dt"], tz=datetime.timezone.utc)
            month = date.month
            day = date.day
            temp = observation["main"]["temp"]
            temp_max = observation["main"]["temp_max"]
            temp_min = observation["main"]["temp_min"]
            hour_above_user_temp = 0

            if temp > user_temp:
                hour_above_user_temp = 1

            if city not in monthly_data:
                monthly_data[city] = {}

            if month not in monthly_data[city]:
                monthly_data[city][month] = {}

            if day not in monthly_data[city][month]:
                monthly_data[city][month][day] = {"high_temp": [temp_max],
                                            "low_temp": [temp_min],
                                            "num_hours_above_user_temp": hour_above_user_temp,
                                            "observations_num": 1}

            else:
                monthly_data[city][month][day]["high_temp"].append(temp_max)
                monthly_data[city][month][day]["low_temp"].append(temp_min)
                monthly_data[city][month][day]["num_hours_above_user_temp"] += hour_above_user_temp
                monthly_data[city][month][day]["observations_num"] += 1

    
    # GENERATE SUMMARY DATA
    monthly_summary = {}
    daily_summary = {}
    hourly_summary = {}

    for city, months in monthly_data.items():
        for month, days in months.items():
            high_temps = []
            low_temps = []
            num_hours_above_user_temp = 0
            observations_num = 0

            for day, data in days.items():
                high_temps.extend(data['high_temp'])
                low_temps.extend(data['low_temp'])
                num_hours_above_user_temp += data['num_hours_above_user_temp']
                observations_num += data['observations_num']

                for hour in range(24):
                    if city not in hourly_summary:
                        hourly_summary[city] = {}
                    
                    if month not in hourly_summary[city]:
                        hourly_summary[city][month] = {}
                    
                    if hour not in hourly_summary[city][month]:
                        hourly_summary[city][month][hour] = []
                    
                    try:
                        hourly_summary[city][month][hour].append(data['high_temp'][hour])
                        hourly_summary[city][month][hour].append(data['low_temp'][hour])
                    except:
                        pass

                if city not in daily_summary:
                    daily_summary[city] = {}
                
                if month not in daily_summary[city]:
                    daily_summary[city][month] = {}

                if day not in daily_summary[city][month]:
                    daily_summary[city][month][day] = {}

                daily_summary[city][month][day]['avg_low_temp'] = sum(data['low_temp']) / len(data['low_temp'])
                daily_summary[city][month][day]['avg_high_temp'] = sum(data['high_temp']) / len(data['high_temp'])
                daily_summary[city][month][day]['num_hours_above_user_temp'] = data['num_hours_above_user_temp']
                daily_summary[city][month][day]['observations_num'] = data['observations_num']

            if city not in monthly_summary:
                monthly_summary[city] = {}
            
            if month not in monthly_summary[city]:
                monthly_summary[city][month] = {}
            
            monthly_summary[city][month]['avg_low_temp'] = sum(low_temps) / len(low_temps)
            monthly_summary[city][month]['avg_high_temp'] = sum(high_temps) / len(high_temps)
            monthly_summary[city][month]['num_hours_above_user_temp'] = num_hours_above_user_temp
            monthly_summary[city][month]['observations_num'] = observations_num


        
    # GENERATE MONTHLY SUMMARY DATAFRAME
    df_list = []
    for city, months in monthly_summary.items():
        for month, stats in months.items():
            stats['city'] = city
            stats['month'] = month
            df_list.append(stats)

    df_monthly = pd.DataFrame(df_list)
    df_monthly.set_index('city', inplace=True)

    # GENERATE DAILY SUMMARY DATAFRAME
    df_list = []
    for city, months in daily_summary.items():
        for month, days in months.items():
            for day, stats in days.items():
                stats['city'] = city
                stats['month'] = month
                stats['day'] = day
                df_list.append(stats)

    df_daily = pd.DataFrame(df_list)

    # GENERATE HOURLY SUMMARY DATAFRAME
    df_list = []
    for city, months in hourly_summary.items():
        for month, hours in months.items():
            for hour, temps in hours.items():
                for temp in temps:
                    stats = {}
                    stats['city'] = city
                    stats['month'] = month
                    stats['hour'] = hour
                    stats['temperature'] = temp
                    df_list.append(stats)

    df_hourly = pd.DataFrame(df_list)


    # DISPLAY MONTHLY SUMMARY 
    st.header("Weather Summary for all BYU Locations")
    st.write("The following table displays historical weather data for all three cities that includes:")      
    st.write("- The average daily high temperature for the month.")
    st.write("- The average daily low temperature for the month.")
    st.write("- The number of observations at each location.")
    st.write("- The number of hours in the month the temperature is above a user input value.")
    st.table(df_monthly.rename(columns={
        "avg_low_temp": "Avg. Low Temp",
        "avg_high_temp": "Avg. High Temp",
        "num_hours_above_user_temp": "Hours Above User Temp",
        "observations_num": "Observations"
        }).drop(["month"], axis=1))



    # DISPLAY DAILY HIGHS 
    st.header("Daily Highs for all BYU Locations")

    # Create a multiselect widget for cities
    cities = byu_locations.keys()
    selected_cities = st.multiselect('Select cities', cities, default=cities)

    
    df_filtered = df_daily[df_daily['city'].isin(selected_cities)]

    base = alt.Chart(df_filtered, title="All BYU Locations Avg. High Temperature Comparison").encode(
        alt.Color('city:N')
    ).properties(
        width=600,
        height=400
    )

    high_temp_line = base.mark_line().encode(x="day:O", y="avg_high_temp:Q")

    chart = (high_temp_line).encode(
        y=alt.Y('avg_high_temp:Q', axis=alt.Axis(title='Temperature (F)')),
        x=alt.X('day:O', axis=alt.Axis(title='Days'))
    )
    
    st.altair_chart(chart, use_container_width=True)



    # DISPLAY DAILY LOWS
    st.header("Temperature Variation by Hour for all BYU Locations")

    # BYU Idaho
    st.markdown("### BYU Idaho")

    min_hour = int(df_hourly['hour'].min())
    max_hour = int(df_hourly['hour'].max())

    hours_byui = st.slider('Select hour range', min_hour, max_hour, (min_hour, max_hour), key="byui")

    base_hourly = alt.Chart(df_hourly[(df_hourly['city'] == "BYU Idaho") & (df_hourly['hour'].astype(int).between(hours_byui[0], hours_byui[1]))]).properties(
        width=600,
        height=400
    )

    temp_box = base_hourly.mark_boxplot(extent="min-max").encode(
        x=alt.X("hour:O", axis=alt.Axis(title='Hours')),
        y=alt.Y("temperature:Q", axis=alt.Axis(title='Temperature (F)'))
    )
   
    st.altair_chart(temp_box, use_container_width=True)

    
    # BYU Provo
    st.markdown("### BYU Provo")

    hours_byup = st.slider('Select hour range', min_hour, max_hour, (min_hour, max_hour), key="byup")

    base_hourly = alt.Chart(df_hourly[(df_hourly['city'] == "BYU Provo") & (df_hourly['hour'].astype(int).between(hours_byup[0], hours_byup[1]))]).properties(
        width=600,
        height=400
    )

    temp_box = base_hourly.mark_boxplot(extent="min-max", color="#A26769").encode(
        x=alt.X("hour:O", axis=alt.Axis(title='Hours')),
        y=alt.Y("temperature:Q", axis=alt.Axis(title='Temperature (F)'))
    )

    st.altair_chart(temp_box, use_container_width=True)


    # BYU Hawaii
    st.markdown("### BYU Hawaii")
    hours_byuh = st.slider('Select hour range', min_hour, max_hour, (min_hour, max_hour), key="byuh")
    
    base_hourly = alt.Chart(df_hourly[(df_hourly['city'] == "BYU Hawaii") & (df_hourly['hour'].astype(int).between(hours_byuh[0], hours_byuh[1]))]).properties(
        width=600,
        height=400
    )

    temp_box = base_hourly.mark_boxplot(extent="min-max", color="#8cd867").encode(
        x=alt.X("hour:O", axis=alt.Axis(title='Hours')),
        y=alt.Y("temperature:Q", axis=alt.Axis(title='Temperature (F)'))
    )

    st.altair_chart(temp_box, use_container_width=True)


