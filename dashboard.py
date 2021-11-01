'''If you use Python 3.6, make sure you run <pip install jinja2==2.11> before running these imports.'''

import os
import pandas as pd
import numpy as np
import json
import streamlit as st
import altair as alt
from streamlit_folium import folium_static
import folium
import pickle
from branca.colormap import linear, LinearColormap
import pydeck as pdk
from dateutil.relativedelta import relativedelta # to add days or years
import datetime as dt



#@st.cache  #Decorator caching data for faster runtimes
def read_data_from_pickles(locations):
    '''Read rainfall data and predictions from pickle file.'''

    with open(r'C:\Users\CAS85405\python-dash-example\Dash-LSTM-rainfall\results\evaluation\eval.pkl', 'rb') as f:
        data = pickle.load(f)

    # Extract data for all locations
    values = {}

    for location in locations:
        predictions = data[location][0]
        training_data = data[location][4]['rain_mm'].values
        training_timeline = data[location][4]['timestamp'].values
        prediction_timeline = data[location][5]['timestamp'].values

        # Combine timelines
        timeline = np.concatenate([training_timeline, prediction_timeline])

        # Aggregate past data
        past = pd.DataFrame(index=range(0, len(training_timeline)))
        past['date'] = training_timeline
        past['rain (mm)'] = training_data
        past['type'] = 'historic'

        # Aggregate future data
        future = pd.DataFrame(index=range(0, len(prediction_timeline)))
        future['date'] = prediction_timeline
        future['rain (mm)'] = predictions
        future['type'] = 'predicted'

        to_plot = pd.concat([past,future], axis=0)

        values[location] = to_plot

    return  values


@st.cache
def read_coordinates():
    '''Read coordinates from file.'''

    base_file = pd.read_csv(r'C:\Users\CAS85405\python-dash-example\Dash-LSTM-rainfall\data\LOCATIONS.csv')

    # Extract data for all locations
    coordinates = {}

    for index, row in base_file.iterrows():
        location = row['Station']
        latitude = row['Lat']
        longitude = row['Lon']

        coordinates[location.lower()] = [latitude, longitude]

    return coordinates


@st.cache(allow_output_mutation=True)
def make_graphs(values, allow_output_mutation=True):
    '''Create graphs for individual locations for Viz #1.'''

    # Single location
    def single_location_graph(location):

        to_plot = values[location]
        loc = location.capitalize()
        graph = alt.Chart(data=to_plot, mark="line", title="Avg monthly rainfall for: "+loc).encode(
                          x=alt.X('date'), 
                          y=alt.Y('rain (mm)', scale=alt.Scale(domain=[0, 250])), 
                          color='type', 
                          strokeDash='type').properties(padding=0, autosize=alt.AutoSizeParams(
        type='pad', contains='content'))

        return graph

    # Produce graphs iteratively
    output = {}

    for location in values.keys():
        
        output[location] = single_location_graph(location)

    return output 

    
@st.cache(hash_funcs={folium.folium.Map: lambda _: None}, allow_output_mutation=True)
def make_map1(values, coordinates):
    '''Create map for Viz #1.'''

    # Create base map
    map1 = folium.Map(location=(51.65, 0.5), zoom_start=7, width='100%', height='100%')

    # Add location markers
    for location in coordinates.keys():

        lat = coordinates[location][0]
        lon = coordinates[location][1]

        # Add location markers
        folium.CircleMarker(location=[lat,lon], radius=6, tooltip=location, color='red', fill=True, fill_color='red',
                            popup = folium.Popup(max_width='100%').add_child(
                                            folium.features.VegaLite(make_graphs(values)[location])
                                            )).add_to(map1)

    return map1


def prepare_data_for_map2(values, coordinates):
    '''Prepare data for Viz #2.
       The input is a dictionary of dataframes and one of coordinates.
       The output is a dataframe with the following structure:

       date | location | lat | lon | rain (mm) | type
    
    '''

    # Empty container
    container = []

    # Iterate over dictionary of dfs
    for location, dataframe in values.items():
        df = dataframe
        df['location'] = location
        df['lat'] = coordinates[location][0]
        df['lon'] = coordinates[location][1]
        df = df[['date','location','lat','lon','rain (mm)','type']]

        container.append(df)

    # Concat dfs
    prepared_data = pd.concat(container, axis=0).sort_values(by='date', ascending=True).reset_index(drop=True)

    return prepared_data


def make_map2(data, lat, lon, zoom):
    '''Create map for Viz #2.'''

    column_layer = pdk.Layer(
                             "ColumnLayer",
                             data=data,
                             get_position=["lon", "lat"],
                             #get_evelation="rain (mm)",
                             elevation_scale=20,
                             radius=2000,
                             get_fill_color=[180, 0, 200, 140],
                             pickable=True,
                             auto_highlight=True,
                             extruded=True
    )

    tooltip={'html': 'Location: {location}</br> Date: {date} </br> Rainfall (mm): {rain_mm}</br> Type: {type}'}

    r = pdk.Deck(column_layer,
                 initial_view_state={
                                    "latitude": lat,
                                    "longitude": lon,
                                    "zoom": zoom,
                                    "pitch": 60
                                },
                 tooltip=tooltip,
                 map_provider="mapbox",
                 map_style='mapbox://styles/mapbox/light-v9',
                )

    map2 = st.write(r)

    return map2


def add_time_slider(format, start_date_str, end_date_str):
    '''Add time slider to Viz #2.
       Provide start and end dates as strings: 'YYYY-MM-DD'.
    '''

    # Dimensions
    cols1,_ = st.columns((2,2)) #Increase second value to get a narrower slider

    # Define format. Available values can be 'MMM YYYY', 'DD MMM YYYY', 'MMM DD, YYYY'
    format = format

    # Define start and end dates
    start_date = dt.date(year=int(start_date_str[0:4]), month=int(start_date_str[5:7]), day=int(start_date_str[8::]))
    end_date = dt.date(year=int(end_date_str[0:4]), month=int(end_date_str[5:7]), day=int(end_date_str[8::]))

    # Create slider and add it to map, returning the selected data
    selected_date = st.slider(
     'Select date',
     min_value=start_date, max_value=end_date,
     value=dt.date(2000,1,15), 
     format=format)

    return selected_date



#==== Initial set up common to all maps
root = os.path.abspath(os.path.join("__file__", "../"))
locations = ['cambridge', 'eastbourne', 'lowestoft', 'heathrow', 'manston', 'oxford']
values = read_data_from_pickles(locations)
coordinates = read_coordinates()


#============================================= VIZ 1
map1 = make_map1(values=values, coordinates=coordinates)

#==== Create title and introductive text
st.header("Digital Solutions for Civil Engineering: Machine Learning + interactive viz")
st.write("""
by Francesco Castellani (mailto:fr.caste.eng@gmail.com)

This page shows an example of how data, predictions from a Machine Learning model, and interactive visualizations can live together in the same place. 

---

This example uses monthly average rainfal data collected by the MetOffice for 6 locations in England:
- Cambridge
- Eastbourne
- Heathrow
- Lowestoft
- Manston
- Oxford

The structure of this app is shown here: https://github.com/FaCoffee1984/Dash-LSTM-rainfall

The data are freely available at: 
https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data 

---
""")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.header("Viz #1: interactive map showing rainfall time series")
st.write("""
Click on each station to visualize the historic rainfall time series (in blue) and the predicted values (in orange). 
""")

# Render map 1 on the app
folium_static(map1, width=800, height=600)
st.write("""---""")


#============================================= VIZ 2
st.header("Viz #2: interactive map showing rainfall as bars")
st.write("""
Move the time slider to visualize how the rainfall values change from one location to another and in relation to each other. 
""")

# Add time slider
start_date_str = '2000-01-15'
end_date_str = '2021-09-15'
format = 'MMM YYYY'
selected_date = add_time_slider(format=format, start_date_str=start_date_str, end_date_str=end_date_str)
st.write("Date selected: ", selected_date)

# Get prepared data and filer by date selected
prepared_data = prepare_data_for_map2(values=values, coordinates=coordinates)
data = prepared_data[prepared_data['date'] == pd.to_datetime(selected_date)]

# Add map
central_location = [51.65, 0.5]
map2 = make_map2(data=data, lat=central_location[0], lon=central_location[1], zoom=7)






