import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Bidirectional, Dropout


def read_data(filepath):
    '''Read data.'''

    data = pd.read_csv(filepath, parse_dates=['timestamp'], index_col=0)

    return data


def slice_data(data, cutoff1, cutoff2):
    '''Slice data along the temporal axis.
       Cutoff1: how far back in time to go
       Cutoff2: timestamp past which the data are used for validation
    '''

    train = data[(data['timestamp'] >= cutoff1) & (data['timestamp'] < cutoff2)].reset_index(drop=True)
    validation = data[data['timestamp'] >= cutoff2].reset_index(drop=True)

    return train, validation


def extract_data(input_data, column_index):
    '''Extract training data.'''

    data = input_data.iloc[:,column_index:column_index+1].values # Return a 2D numpy array

    return data


def scale_data(data):
    '''Apply feature scaling.'''

    sc = StandardScaler(with_mean=True, with_std=True)
    scaled = sc.fit_transform(data)

    return scaled


def train_time_windows(scaled_data, n_past, n_future):
    '''Define two temporal windows: past and future, with different sizes, relative to each month in the time series.'''

    # Empty windows
    past = [] 
    future = [] 

    # Populate empty windows
    # This creates one window with x values (x/12 years) before a given month
    # and one window with y values (y/12 years) ahead of a given month
    # "0" means that the first (and only) numerical value in the numpy array is appened to the list
    for i in range(0, len(scaled_data)-n_past-n_future+1):
        past.append(scaled_data[i : i + n_past, 0]) 
        future.append(scaled_data[i + n_past : i + n_past + n_future, 0])

    # Turn lists into numpy arrays
    past, future = np.array(past), np.array(future)

    # Reshape
    # "1" means that the array will be 2D
    past = np.reshape(past, (past.shape[0], past.shape[1], 1))

    return past, future


def pipeline(filepath, cutoff1, cutoff2, column_index, n_past, n_future):
    '''Apply pipeline to input data. 
       Steps:
       - 1. Read data
       - 2. Slice data (ignore data that are too old)
       - 3. Extract data
       - 4. Scale train data
       - 5. Obtain past and future data
       - 6. Return values
    '''

    result1 = read_data(filepath=filepath)
    result2, validation = slice_data(result1, cutoff1=cutoff1, cutoff2=cutoff2)
    result2, validation = extract_data(result2, column_index=column_index), extract_data(validation, column_index=column_index)
    result2 = scale_data(result2)

    past, future = train_time_windows(result2, n_past, n_future)

    return past, future, validation


def fit_lstm(n_past, n_future, past_train, future_train, n_epochs):
    '''Initialise Keras LSTM model.'''

    # Initialise regressor
    regressor = Sequential()

    #==== LAYER 1 (HIDDEN LAYER)
    # Add bidirectional LSTM with n_past memory units, 1 for each month in the n_past window
    regressor.add(Bidirectional(LSTM(units=n_past, return_sequences=True, input_shape=(past_train.shape[1],1))))
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
    regressor.compile(optimizer='nadam', loss='mean_squared_error', metrics=['acc'])

    # Fit model and store loss & accuracy information
    history = regressor.fit(past_train, future_train, epochs=n_epochs, batch_size=32)

    return regressor, history


def model_performance(n_past, n_future, past_train, future_train, n_epochs):
    '''Fit LSTM models and capture training performance.'''

    model, history = fit_lstm(n_past=n_past, n_future=n_future, past_train=past_train, future_train=future_train, n_epochs=n_epochs)

    acc = history.history['acc']
    loss = history.history['loss']

    return model, history, acc, loss


def plot_performance():
    '''Plot model accuracy an dlosses during training.'''

    return


def evaluate(validation, model):
    '''Compute MRSE during evaluation and plot.'''

    return


def serialise(dict):
    '''Create pickle file from dictionary.'''

    return


# Set root dir
root = os.path.abspath(os.path.join("__file__", "../.."))

# Data ingestion and processing pipeline; "rain_mm" has column_index=4
cutoff1 = '2000-01-15'
cutoff2 = '2018-01-15'

n_past = 120
n_future = 24
column_index = 4
n_epochs = 500

locations = ['cambridge','eastbourne','heathrow','lowestoft','manston','oxford']

container = {}

for location in locations:

    print('Location: '+location)

    # Identify correct filepath
    filepath = root + '/data/clean/'+str(location)+'.csv'

    # Extract past, future, validation datasets
    print('Extracting past, future, validation datasets')
    past, future, validation = pipeline(filepath=filepath, cutoff1=cutoff1, cutoff2=cutoff2, 
                                        column_index=column_index, n_past=n_past, n_future=n_future)

    # Fit model and compute performance
    print('Fitting model')
    model, history, acc, loss = model_performance(n_past=n_past, n_future=n_future, past_train=past, future_train=future, n_epochs=n_epochs)

    print('Storing everything in container')
    container[location] = [model, history, acc, loss]






# Plot accuracy and losses
acc = history['acc']
loss = history['loss']
plt.plot(range(0,n_epochs), acc, label='acc')
plt.plot(range(0,n_epochs), loss, label='loss', color='red')
plt.legend()
plt.xlabel("Epochs")
plt.ylabel("Values")
plt.ylim(0,1.0)
plt.title("Accuracy vs loss for Cambridge")