#%%
import calendar
import datetime
import json
import pprint

import pandas as pd
from requests import request




byu_locations = {"BYU Idaho": {"lat": 43.825386, "lon": -111.792824},
                 "BYU Provo": {"lat":  40.233845, "lon": -111.658531},
                 "BYU Hawaii": {"lat": 21.648287, "lon": -157.922562}
                 }

# byu_locations = {"BYU Idaho": {"lat": 43.815982, "lon": -111.784748}}

months = {
    "October 2023": {"month": 10, "year": 2023},
    "November 2023": {"month": 11, "year": 2023},
    "December 2023": {"month": 12, "year": 2023},
    "January 2024" : {"month": 1, "year": 2024},
    "February 2024" : {"month": 2, "year": 2024},
    "March 2024" : {"month": 3, "year": 2024},
    }

## USER INPUTS
api_key = '' # this is selected by the user
city = 'BYU Idaho' # this is selected by the user
# TODO: Check when month is 5 - 10, requested data is out of allowed range
# month_end = 10 # this is selected by the user
user_temp = 45 # this is selected by the user


month_user= "October 2023"
year = months[month_user]["year"]
month = months[month_user]["month"]
_, last_day = calendar.monthrange(year, month)





# month_start = (month_end - 6) if (month_end - 6) > 0 else 12 + (month_end - 6)
# current_month = datetime.datetime.now().month
# current_year = datetime.datetime.now().year
# year_start = 0
# year_end = 0
# last_day = 0
# api_url = ""
# lat = ""
# lon = ""

# if 1 <= month_end <= current_month:
#     year_end= current_year 
# else:
#     year_end = current_year - 1

# if month_end >= month_start:
#     year_start = year_end
# else:
#     year_start = year_end - 1

# if month_end == current_month:
#     last_day = datetime.datetime.now().day - 1
# else:
#     _, last_day = calendar.monthrange(year_end, month_end)


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

print(all_cities)

#%%

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

print(monthly_data)
# save monthly_data to a json file
with open("monthly_data.json", "w") as file:
    json.dump(monthly_data, file)


#%%
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


with open("hourly_summary.json", "w") as file:
    json.dump(hourly_summary, file)

    
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


# DAILY HIGHS AND LOWS OVER A MONTH
import altair as alt

base = alt.Chart(df_daily, title="All BYU Locations Avg. High Temperature Comparison").encode(
    alt.Color('city:N')
).properties(
    width=600,
    height=400
)

high_temp_line = base.mark_line().encode(x="day:O", y="avg_high_temp:Q")
# low_temp_line = base.mark_line(color="blue").encode(x="day:O", y="avg_low_temp:Q")
chart = (high_temp_line).encode(
    y=alt.Y('avg_high_temp:Q', axis=alt.Axis(title='Temperature (F)')),
    x=alt.X('day:O', axis=alt.Axis(title='Days'))
)
chart


base_hourly = alt.Chart(df_hourly[df_hourly.city == "BYU Idaho"], title="BYU Idaho: Temperature Variation by Hour").properties(
    width=600,
    height=400
)

temp_box = base_hourly.mark_boxplot(extent="min-max").encode(
    x=alt.X("hour:O", axis=alt.Axis(title='Hours')),
    y=alt.Y("temperature:Q", axis=alt.Axis(title='Temperature (F)'))
)


base_hourly = alt.Chart(df_hourly[df_hourly.city == "BYU Provo"], title="BYU Provo: Temperature Variation by Hour").properties(
    width=600,
    height=400
)

temp_box = base_hourly.mark_boxplot(extent="min-max", color="#A26769").encode(
    x=alt.X("hour:O", axis=alt.Axis(title='Hours')),
    y=alt.Y("temperature:Q", axis=alt.Axis(title='Temperature (F)'))
)

temp_box






# %%
