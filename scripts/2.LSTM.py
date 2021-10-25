import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input,
    Dense,
    LSTM,
    AveragePooling1D,
    TimeDistributed,
    Flatten,
    Bidirectional,
    Dropout
)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


def read_data(filepath):
    '''Read data.'''

    data = pd.read_csv(filepath, parse_dates=['timestamp'], index_col=0)

    return data


def slice_data(data, cutoff):
    '''Slice data along the temporal axis.'''

    data = data[data['timestamp'] >= cutoff].reset_index(drop=True)

    return data


def train_data(data, column_index):
    '''Extract training data.'''

    train = data.iloc[:,column_index:column_index+1].values # Return a 2D numpy array

    return train


def scale_data(train):
    '''Apply feature scaling between 0 and 1.'''

    sc = MinMaxScaler(feature_range=(0,1))
    scaled = sc.fit_transform(train)

    return scaled


def train_time_windows(scaled_data, n_past, n_future):
    '''Define two temporal windows: past and future, with different sizes, relative to each month in the time series.'''

    # Empty windows
    x_train = [] # past
    y_train = [] # future

    # Populate empty windows
    # This creates one window with x values (x/12 years) before a given month
    # and one window with y values (y/12 years) ahead of a given month
    # "0" means that the first (and only) numerical value in the numpy array is appened to the list
    for i in range(0, len(scaled_data)-n_past-n_future+1):
        x_train.append(scaled_data[i : i + n_past, 0]) 
        y_train.append(scaled_data[i + n_past : i + n_past + n_future, 0])

    # Turn lists into numpy arrays
    x_train , y_train = np.array(x_train), np.array(y_train)

    # Reshape
    # "1" means that the array will be 2D
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    return x_train, y_train


def fit_model(n_past, n_future, x_train, y_train):
    '''Initialise Keras LSTM model.'''

    # Initialise regressor
    regressor = Sequential()

    #==== LAYER 1 (HIDDEN LAYER)
    # Add bidirectional LSTM with n_past memory units, 1 for each month in the n_past window
    regressor.add(Bidirectional(LSTM(units=n_past, return_sequences=True, input_shape=(x_train.shape[1],1))))
    # Add dropout to prevent overfitting
    regressor.add(Dropout(rate=0.2))

    #==== LAYER 2 (HIDDEN LAYER)
    regressor.add(LSTM(units=n_past, return_sequences=True))
    regressor.add(Dropout(rate=0.2))

    #==== LAYER 3 (HIDDEN LAYER)
    regressor.add(LSTM(units=n_past, return_sequences=True))
    regressor.add(Dropout(rate=0.2))

    #==== LAYER 4 (HIDDEN LAYER)
    regressor.add(LSTM(units=n_past))
    regressor.add(Dropout(rate=0.2))

    #==== LAYER 5 (OUTPUT LAYER)
    # This layer contains a linear activation function that outputs n_future values
    # This is used to make sure that output values are proportional to the input (eg, same value range)
    regressor.add(Dense(units=n_future, activation='linear'))

    # Compile model
    regressor.compile(optimizer='adam', loss='mean_squared_error', metrics=['acc'])

    # Fit model
    history = regressor.fit(x_train, y_train, epochs=50, batch_size=32)

    return regressor, history





# Set root dir
root = os.path.abspath(os.path.join("__file__", "../.."))

# Data ingestion and processing pipeline; "rain_mm" has column_index=4
cutoff = '2000-01-15'
cambridge = scale_data(train_data(slice_data(read_data(filepath=root+'/data/clean/cambridge.csv'), cutoff=cutoff), column_index=4))
eastbourne = scale_data(train_data(slice_data(read_data(filepath=root+'/data/clean/eastbourne.csv'), cutoff=cutoff), column_index=4))
heathrow = scale_data(train_data(slice_data(read_data(filepath=root+'/data/clean/heathrow.csv'), cutoff=cutoff), column_index=4))
lowestoft = scale_data(train_data(slice_data(read_data(filepath=root+'/data/clean/lowestoft.csv'), cutoff=cutoff), column_index=4))
manston = scale_data(train_data(slice_data(read_data(filepath=root+'/data/clean/manston.csv'), cutoff=cutoff), column_index=4))
oxford = scale_data(train_data(slice_data(read_data(filepath=root+'/data/clean/oxford.csv'), cutoff=cutoff), column_index=4))

# Assumption: given 10 years of monthly values (120 values), predict the next 2 years (24 values)
n_past = 120
n_future = 24
cbg_train_past, cbg_train_future = train_time_windows(cambridge, n_past=n_past, n_future=n_future)
eas_train_past, eas_train_future = train_time_windows(eastbourne, n_past=n_past, n_future=n_future)
lhr_train_past, lhr_train_future = train_time_windows(heathrow, n_past=n_past, n_future=n_future)
low_train_past, low_train_future = train_time_windows(lowestoft, n_past=n_past, n_future=n_future)
man_train_past, man_train_future = train_time_windows(manston, n_past=n_past, n_future=n_future)
oxf_train_past, oxf_train_future = train_time_windows(oxford, n_past=n_past, n_future=n_future)

# Fit model
cbg_model, cbg_history = fit_model(n_past=n_past, n_future=n_future, x_train=cbg_train_past, y_train=cbg_train_future)