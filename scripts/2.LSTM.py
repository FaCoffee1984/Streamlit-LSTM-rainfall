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

    train = data.iloc[:,column_index:column_index+1].values # Return a 2D array

    return train


def scale_data(train):
    '''Apply feature scaling.'''

    sc = MinMaxScaler(feature_range=(0,1))
    scaled = sc.fit_transform(train)

    return scaled


# Set root dir
root = os.path.abspath(os.path.join("__file__", "../.."))

# Data ingestion and processing pipeline; rain_mm has column_index=4
cutoff = '2000-01-15'
cambridge = scale_data(train_data(slice_data(read_data(filepath=root+'/data/clean/cambridge.csv'), cutoff=cutoff), column_index=4))
eastbourne = scale_data(train_data(slice_data(read_data(filepath=root+'/data/clean/eastbourne.csv'), cutoff=cutoff), column_index=4))
heathrow = scale_data(train_data(slice_data(read_data(filepath=root+'/data/clean/heathrow.csv'), cutoff=cutoff), column_index=4))
lowestoft = scale_data(train_data(slice_data(read_data(filepath=root+'/data/clean/lowestoft.csv'), cutoff=cutoff), column_index=4))
manston = scale_data(train_data(slice_data(read_data(filepath=root+'/data/clean/manston.csv'), cutoff=cutoff), column_index=4))
oxford = scale_data(train_data(slice_data(read_data(filepath=root+'/data/clean/oxford.csv'), cutoff=cutoff), column_index=4))





