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



@st.cache  #Decorator caching data for faster runtimes
def read_data_from_pickles(locations):

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
def make_map(values, coordinates):

    # Create base map
    main_map = folium.Map(location=(51.65, 0.5), zoom_start=7, width='100%', height='100%')

    # Add location markers
    for location in coordinates.keys():

        lat = coordinates[location][0]
        lon = coordinates[location][1]

        # Add location markers
        folium.CircleMarker(location=[lat,lon], radius=6, tooltip=location, color='red', fill=True, fill_color='red',
                            popup = folium.Popup(max_width='100%').add_child(
                                            folium.features.VegaLite(make_graphs(values)[location])
                                            )).add_to(main_map)

    return main_map


#==== Initial parameters
root = os.path.abspath(os.path.join("__file__", "../"))
locations = ['cambridge', 'eastbourne', 'lowestoft', 'heathrow', 'manston', 'oxford']


#============================================= VIZ 1
values = read_data_from_pickles(locations)
coordinates = read_coordinates()
main_map1 = make_map(values=values, coordinates=coordinates)

#==== Create title and introductive text
st.header("Digital Solutions for Civil Engineering: combining Machine Learning with interactive viz")
st.write("""
by Francesco Castellani (mailto:fr.caste.eng@gmail.com)

This page shows an example of how data, predictions from a Machine Learning model, and interactive visualizations can live together. 
This example uses monthly average rainfal data collected by the MetOffice for 6 locations in England.

---

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
folium_static(main_map1, width=800, height=600)
st.write("""---""")


#============================================= VIZ 2
st.header("Viz #2: interactive map showing rainfall as bars")
st.write("""
Move the time slider to visualize how the rainfall values change from one location to another and in relation to each other. 
""")


