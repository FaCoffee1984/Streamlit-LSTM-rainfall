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


root = os.path.abspath(os.path.join("__file__", "../"))

locations = ['cambridge', 'eastbourne', 'lowestoft', 'heathrow', 'manston', 'oxford']


@st.cache  #Decorator caching data for faster runtimes
def read_data_from_pickles(locations):

    with open('./Dash-LSTM-rainfall/results/evaluation/eval.pkl', 'rb') as f:
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

    base_file = pd.read_csv('./Dash-LSTM-rainfall/data/LOCATIONS.csv')

    # Extract data for all locations
    coordinates = {}

    for index, row in base_file.iterrows():
        location = row['Station']
        latitude = row['Lat']
        longitude = row['Lon']

        coordinates[location] = [latitude, longitude]

    return coordinates


@st.cache(allow_output_mutation=True)
def make_graphs(values, location, allow_output_mutation=True):

    # Single location
    def single_location_graph(location):

        to_plot = values[location]
        graph = alt.Chart(data=to_plot, mark="line", title="Avg monthly rainfall for: "+location.capitalize()).encode(
                          x=alt.X('date'), 
                          y=alt.Y('rain (mm)', scale=alt.Scale(domain=[0, 250])), 
                          color='type', 
                          strokeDash='type')

        return graph

    


@st.cache(hash_funcs={folium.folium.Map: lambda _: None}, allow_output_mutation=True)
def make_map(coordinates):

    # Create base map
    main_map = folium.Map(location=(51.65, 0.5), zoom_start=7)

    # Add location markers
    for location in coordinates.keys():

        lat = coordinates[location][0]
        lon = coordinates[location][1]

        # Add location markers
        folium.CircleMarker(location=[lat,lon],radius=5, tooltip=location, color='red', fill=True, fill_color='red',
                            popup = folium.Popup().add_child(
                                            folium.features.VegaLite(json.dumps(np.arange(0,10,1),default=default))
                                            )).add_to(main_map)

    return main_map



    colormap = linear.RdYlBu_08.scale(station_stats[field_to_color_by].quantile(0.05),
                                      station_stats[field_to_color_by].quantile(0.95))
    if reverse_colormap[field_to_color_by]:
        colormap = LinearColormap(colors=list(reversed(colormap.colors)),
                                  vmin=colormap.vmin,
                                  vmax=colormap.vmax)
    colormap.add_to(main_map)
    metric_desc = metric_descs[field_to_color_by]
    metric_unit = metric_units[field_to_color_by]
    colormap.caption = metric_desc
    colormap.add_to(main_map)
    for _, city in station_stats.iterrows():
        icon_color = colormap(city[field_to_color_by])
        city_graph = city_graphs['for_map'][city.station_id][field_to_color_by]
        folium.CircleMarker(location=[city.lat, city.lon],
                    tooltip=f"{city.municipality}\n  value: {city[field_to_color_by]}{metric_unit}",
                    fill=True,
                    fill_color=icon_color,
                    color=None,
                    fill_opacity=0.7,
                    radius=5,
                    popup = folium.Popup().add_child(
                                            folium.features.VegaLite(city_graph)
                                            )
                    ).add_to(main_map)
    return main_map




#==== Create title and introductive text
st.header("Title")
st.write("""
Introduction
""")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
