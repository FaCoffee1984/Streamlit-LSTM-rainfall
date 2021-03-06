import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Bidirectional, Dropout


def read_data(filepath):
    '''Read data.'''

    data = pd.read_csv(filepath, parse_dates=['timestamp'], index_col=0)

    return data


def slice_data(data, cutoff1, n_future):
    '''Slice data along the temporal axis.
       Cutoff1: how far back in time to go (eg, '1986-02-15')
       n_future: length of the future predictions (used for predictions and validation)
    '''

    # Select train data between the cutoff and the end of the time series MINUS the length of the future window (see "past_future_windows")
    data = data[(data['timestamp'] >= cutoff1)]
    train = data.head(len(data)-n_future).reset_index(drop=True)

    # Select validataion data to be the last n_future records of the input data
    validation = data.tail(n_future).reset_index(drop=True)

    return train, validation


def extract_data(input_data, column_index):
    '''Extract training data.'''

    data = input_data.iloc[:,column_index:column_index+1].values # Return a 2D numpy array

    return data


def scale_data(data):
    '''Apply feature scaling.'''

    # Initialise and apply scaler
    sc = StandardScaler(with_mean=True, with_std=True)
    scaled = sc.fit_transform(data)

    return scaled, sc


def past_future_windows(scaled_data, n_past, n_future):
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


def pipeline(filepath, cutoff1, column_index, n_past, n_future):
    '''Apply pipeline to input data. 
       Steps:
       - 1. Read data
       - 2. Slice data (ignore data that are too old) and retrieve timestamps
       - 3. Extract data
       - 4. Scale train data
       - 5. Obtain past and future data
       - 6. Return values
    '''

    # Read data
    result1 = read_data(filepath=filepath)

    # Slice data
    result2, validation = slice_data(result1, cutoff1=cutoff1, n_future=n_future)

    # Retrieve timestamps for future computations/plotting
    result_timestamp, validation_timestamp = result2['timestamp'], validation['timestamp']

    # Extract data
    result2, validation = extract_data(result2, column_index=column_index), extract_data(validation, column_index=column_index)

    # Scale train data only (validation will be scaled by function "evaluate")
    result2, sc = scale_data(result2)

    # Extract past and future values
    past, future = past_future_windows(result2, n_past, n_future)

    return past, future, validation, sc, result_timestamp, validation_timestamp


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

    # Fit models
    model, history = fit_lstm(n_past=n_past, n_future=n_future, past_train=past_train, future_train=future_train, n_epochs=n_epochs)

    # Grab accuracy and loss values
    acc = history.history['acc']
    loss = history.history['loss']

    return model, acc, loss


def process_bulk_locations(locations, cutoff1, column_index, n_past, n_future, n_epochs):
    '''For each location, perform the following steps:
       - 1. Identify filepath
       - 2. Generate past, future, validation datasets and scaler
       - 3. Fit model
       - 4. Store everything in a dictionary
    '''

    # Empty container
    results = {}

    for location in locations:

        print('Location: '+location)

        # Identify correct filepath
        filepath = root + '/data/clean/'+str(location)+'.csv'

        # Extract past, future, validation datasets
        print('Extracting past, future, validation datasets')
        past, future, validation, sc, result_timestamp, validation_timestamp = pipeline(filepath=filepath, cutoff1=cutoff1,  
                                            column_index=column_index, n_past=n_past, n_future=n_future)

        # Fit model and compute performance
        print('Fitting model')
        model, acc, loss = model_performance(n_past=n_past, n_future=n_future, past_train=past, future_train=future, n_epochs=n_epochs)

        print('Storing everything in container')
        results[location] = [model, acc, loss, validation, sc, result_timestamp, validation_timestamp]

    return results


def plot_training_performance(container, n_epochs):
    '''Plot model accuracy and losses during training. 
       "container" is the output of the "process_bulk_locations" function.
    '''

    # Declare final figure
    ax = plt.figure(figsize=(20, 10))

    # Grab x values
    x = range(0, n_epochs)

    for i, location in enumerate(container.keys()):

        acc = container[location][1]
        loss = container[location][2]

        plt.subplot(3, 2, i+1)
        plt.plot(x, loss, color='red', label='loss')
        plt.plot(x, acc, color='navy', label='acc')

        plt.legend()
        plt.xlabel("Epochs")
        plt.ylabel("Values")
        plt.ylim(0,1.0)
        plt.title("Accuracy vs loss for "+location, fontsize=13)
        plt.tight_layout()
        plt.grid("on")

    return ax


def compute_rmse(predictions, validation):
    '''Compute Root Mean Squared Error (RMSE) between two sets of measurements: 
       predictions and validation.
    '''

    # Turn input numpy 2D arrays into flat, 1D arrays
    predictions1d = predictions.flatten()
    validation1d = validation.flatten()

    # Compute RMSE. Squared = True returns the variance.
    rmse = mean_squared_error(predictions1d, validation1d, squared=False)

    return rmse


def evaluate(container):
    '''Evaluate on unseen data, compute MRSE, and plot.'''

    # Declare final figure
    ax = plt.figure(figsize=(20, 10))

    # Empty final container
    evaluation = {}

    for i, location in enumerate(container.keys()):

        # Grab validation data and scaler from each time series
        validation = container[location][3]
        sc = container[location][4]

        # Take validation data and scale them using the same scaler used in training 
        # Because the modele expects to see scaled data as input
        testing = sc.transform(validation)
        # Create numpy array and reshape it like past and future
        testing = np.array(testing)
        testing = np.reshape(testing,(testing.shape[1],testing.shape[0],1))

        # Grab relevant model
        model = container[location][0]

        # Make predictions on the testing data
        predictions = model.predict(testing)

        # Make inverse transformation 
        predictions = sc.inverse_transform(predictions)

        # Reshape to look like validation
        predictions = np.reshape(predictions,(predictions.shape[1],predictions.shape[0]))

        # Compute RMSE
        rmse = round(compute_rmse(predictions, validation),2)

        # Compute difference
        difference = validation - predictions

        # Add values to evaluation dictionary
        evaluation[location] = [predictions, validation, difference, rmse]

        # Plot
        x = container[location][6] #Grab validation timestamps

        plt.subplot(3, 2, i+1)

        plt.plot(x, validation, color='navy', label='validation')
        plt.plot(x, predictions, color='red', label='predictions')

        plt.annotate("RMSE: "+str(rmse), (x[3],202))

        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Rainfall (mm)")
        plt.ylim(0,250)
        plt.title("Predictions vs Validation for: "+location, fontsize=13)
        plt.tight_layout()
        plt.grid("on")


    return evaluation, ax


def serialise_models(training_performance, root):
    '''Save Keras model to filepath using HDF5 extension (.h5).'''

    # Access trained models from training_performance dict
    for i, location in enumerate(training_performance.keys()):
        model = training_performance[location][0]

        # Specify filename
        filename = root+'/models/'+location+"_trained_model.h5"

        # Save model
        model.save(filename)

    return


def serialise_values(dict, root, perf=None, eval=None, cutoff1=None, n_future=None):
    '''Create pickle file from dictionary and save it to filepath.
       Differentiates between training_performance and evaluation dicts.
       One between perf and eval needs to be True.
       PS: If eval=True, "cutoff1" AND "n_future" must be provided.
    '''

    if perf is True:

        # Remove model from dict as it is serialised by the "serialise_models" function
        for i, location in enumerate(dict.keys()):
            del dict[location][0] # Delete model from dict - already serialised

        # Define filename
        filename = root + '/results/training_performance/training_perf.pkl'

        # Dump pickle object
        with open(filename, 'wb') as handle: # 'wb' stands for: write binary
            pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


    if eval is True:

        for i, location in enumerate(dict.keys()):
            filepath = root + '/data/clean/'+str(location)+'.csv'

            # Access training data
            data = read_data(filepath)

            # Slice data
            train, validation = slice_data(data, cutoff1=cutoff1, n_future=n_future)

            # Add train and validation dfs (with timestamps) to evaluation dict
            dict[location].append(train)
            dict[location].append(validation)

        # Define filename
        filename = root + '/results/evaluation/eval.pkl'

        # Dump pickle object
        with open(filename, 'wb') as handle: # 'wb' stands for: write binary
            pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return


# =========== MAIN ===========


# Set root dir
root = os.path.abspath(os.path.join("__file__", "../.."))

# Cutoff dates
cutoff1 = '2000-01-15'
cutoff2 = '2018-01-15'

# Parameters
n_past = 120 #10 years
n_future = 24 #2 years
column_index = 4 #"rain_mm" has column_index=4
n_epochs = 500

# Locations
locations = ['cambridge','eastbourne','heathrow','lowestoft','manston','oxford']

# Bulk processing
training_performance = process_bulk_locations(locations, cutoff1, column_index, n_past, n_future, n_epochs)

# Plot training performance
ax = plot_training_performance(training_performance, n_epochs)

# Evaluation
evaluation, ax = evaluate(training_performance)

# Save serialised models (.h5)
serialise_models(training_performance, root)

# Save serialise training performance values
serialise_values(dict=training_performance, root=root, perf=True)

# Save serialsied evaluation
serialise_values(dict=evaluation, root=root, eval=True, cutoff1=cutoff1, n_future=n_future)