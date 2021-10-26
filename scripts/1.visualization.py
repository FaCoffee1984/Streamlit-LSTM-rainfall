import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def slice_data(data, cutoff):
    '''Slice data along the temporal axis.'''

    data = data[data['timestamp'] >= cutoff]

    return data


# Set root dir
root = os.path.abspath(os.path.join("__file__", "../.."))

# Read clean data
cutoff = '2000-01-15'
cambridge = slice_data(pd.read_csv(root + '/data/clean/cambridge.csv', parse_dates=['timestamp'], index_col=0), cutoff=cutoff) 
eastbourne = slice_data(pd.read_csv(root + '/data/clean/eastbourne.csv', parse_dates=['timestamp'], index_col=0), cutoff=cutoff)
heathrow = slice_data(pd.read_csv(root + '/data/clean/heathrow.csv', parse_dates=['timestamp'], index_col=0), cutoff=cutoff)
lowestoft = slice_data(pd.read_csv(root + '/data/clean/lowestoft.csv', parse_dates=['timestamp'], index_col=0), cutoff=cutoff)
manston = slice_data(pd.read_csv(root + '/data/clean/manston.csv', parse_dates=['timestamp'], index_col=0), cutoff=cutoff)
oxford = slice_data(pd.read_csv(root + '/data/clean/oxford.csv', parse_dates=['timestamp'], index_col=0),cutoff=cutoff)


# Plot
plt.figure(figsize=(20, 10))
plt.subplot(3, 2, 1)
plt.plot(cambridge['timestamp'],cambridge['rain_mm'], color='navy')
plt.xlabel("Time")
plt.ylabel("Rain (mm)")
plt.title("Monthly avg rainfall for Cambridge")

plt.subplot(3, 2, 2)
plt.plot(eastbourne['timestamp'],eastbourne['rain_mm'], color='navy')
plt.xlabel("Time")
plt.ylabel("Rain (mm)")
plt.title("Monthly avg rainfall for Eastbourne")

plt.subplot(3, 2, 3)
plt.plot(heathrow['timestamp'],heathrow['rain_mm'], color='navy')
plt.xlabel("Time")
plt.ylabel("Rain (mm)")
plt.title("Monthly avg rainfall for Heathrow")

plt.subplot(3, 2, 4)
plt.plot(lowestoft['timestamp'],lowestoft['rain_mm'], color='navy')
plt.xlabel("Time")
plt.ylabel("Rain (mm)")
plt.title("Monthly avg rainfall for Lowestoft")

plt.subplot(3, 2, 5)
plt.plot(manston['timestamp'],manston['rain_mm'], color='navy')
plt.xlabel("Time")
plt.ylabel("Rain (mm)")
plt.title("Monthly avg rainfall for Manston")

plt.subplot(3, 2, 6)
plt.plot(oxford['timestamp'],oxford['rain_mm'], color='navy')
plt.xlabel("Time")
plt.ylabel("Rain (mm)")
plt.title("Monthly avg rainfall for Oxford")
