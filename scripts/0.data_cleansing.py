import os
import pandas as pd
from datetime import datetime


def extract_values(line):
    '''Extract numerical values from text lines.'''

    # Split line
    line = line.split('   ')

    # Special characters
    special_chars = ["$", "@", "#", "&", "%", "*", "-", "~", "?", "/", "!"]

    # Year
    time = line[1].split('  ')
    year = int(time[0])

    # Month
    if len(time) > 1:
        month = int(time[1])
    else:
        month = int(line[2])

    # Rain
    if len(line) == 7:
        rain = str(line[4][2:]).replace(" ---","0.00").replace("---","0.00").replace("--- ","0.00")

    if len(line) == 8:
        rain = str(line[6][1:]).replace(" ---","0.00").replace("---","0.00").replace("--- ","0.00")

    if len(line) == 9:
        rain = str(line[7][1:]).replace(" ---","0.00").replace("---","0.00").replace("--- ","0.00")

    if len(line) == 10:
        rain = str(line[8][1:]).replace(" ---","0.00").replace("---","0.00").replace("--- ","0.00")

    # Get rid of special characters
    rain = float("".join([k for k in rain if k not in special_chars]))   
        
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







with open(root + '/data/Eastbourne.txt','rt',encoding='utf-8') as file:
    lines = file.readlines()[2:]

    df = pd.DataFrame(index=range(0, len(lines)), columns=['year','month','rain'])

    for i, line in enumerate(lines):
        line = line.split('   ')
        print(len(line))

        to_append = extract_values(line)







