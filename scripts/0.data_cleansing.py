import os
import pandas as pd
from datetime import datetime
import re


def extract_values(line):
    '''Extract numerical values from text lines.'''

    # Split line
    line_split = line.split('   ')

    # Extract clean items
    clean = [ei for e in line_split for ei in e.strip().split()]

    # Special characters
    special_chars = ["$", "@", "#", "&", "%", "*", "-", "~", "?", "/", "!"]

    # Year
    year = int(clean[0])

    # Month
    month = int(clean[1])

    # Rain
    rain = clean[5].replace(" ---","0.00").replace("---","0.00").replace("--- ","0.00")
    rain = "".join([k for k in rain if k not in special_chars])


    return [year, month, rain]


def file_to_df(filepath):
    '''Turn text file into pandas df.'''

    with open(filepath,'rt',encoding='utf-8') as file:
        lines = file.readlines()[2:]

        # Create empty final df
        result = pd.DataFrame(index=range(0, len(lines)), columns=['year','month','rain'])

        # Iterate over lines of text
        for i, line in enumerate(lines):

            # Generate list of values and append it to df
            to_append = extract_values(line)
            result.iloc[i] = to_append

    # Format data type
    result.year = df.year.astype(int)
    result.month = df.month.astype(int)
    result.rain = df.rain.astype(float)

    # Add timestamp
    result['timestamp'] = result.apply(lambda row: datetime.strptime(f"{int(row.year)}-{int(row.month)}-15", '%Y-%m-%d'), axis=1)
    result = result[['timestamp','year','month','rain']]

    return result


# Set root dir
root = os.path.abspath(os.path.join("__file__", "../../"))

# Read data
# Raw
cambridge_raw = pd.read_csv(root + '/data/Cambridge.txt')
eastbourne_raw = pd.read_csv(root + '/data/Eastbourne.txt')
# Cleaned
cambridge = file_to_df(filepath = root + '/data/Cambridge.txt')
eastbourne = file_to_df(filepath = root + '/data/Eastbourne.txt')







with open(root + '/data/Oxford.txt','rt',encoding='utf-8') as file:
    lines = file.readlines()[2:]

    df = pd.DataFrame(index=range(0, len(lines)), columns=['year','month','rain'])
    lens = []
    for i, line in enumerate(lines):
        print(extract_values(line))









