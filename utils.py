'''Utility functions'''

import os
import pandas as pd
import numpy as np
import pickle
import streamlit as st
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


#@st.cache
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
