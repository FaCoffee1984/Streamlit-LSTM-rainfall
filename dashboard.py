'''If you use Python 3.6, make sure you run <pip install jinja2==2.11> before running these imports.'''

import os
import pandas as pd
import streamlit as st
import altair as alt
from streamlit_folium import folium_static
import folium
import pickle
from branca.colormap import linear, LinearColormap

'''
Meaning of the @st.cache line:
It is a decorator that checks:
1. The input parameters that you called the function with
2. The value of any external variable used in the function
3. The body of the function
4. The body of any function used inside the cached function

MUCH FASTER RUN TIMES!
If this is the first time Streamlit has seen these four components with these exact values 
and in this exact combination and order, it runs the function and stores the result in a local cache. 
The next time the cached function is called, if none of these components changed, 
Streamlit will just skip executing the function altogether and will return the output 
previously stored in the cache.
'''

root = os.path.abspath(os.path.join("__file__", "../"))

locations = ['cambridge', 'eastbourne', 'lowestoft', 'heathrow', 'manston', 'oxford']

@st.cache  
def read_data_from_pickles(location):

    with open('./Dash-LSTM-rainfall/results/evaluation/eval.pkl', 'rb') as f:
        data = pickle.load(f)

    # Extract data for all locations
    values = {}

    for location in locations:
        predictions = data[location][0]
        validation = data[location][1]

        values[location] = [predictions, validation]

    # Extract timeline for plots
    timeline = data['cambridge'][5]['timestamp'].tolist()

    return  values, timeline


@st.cache
def read_coordinates(root):





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
