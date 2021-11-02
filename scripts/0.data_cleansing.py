import os
import pandas as pd
from datetime import datetime


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
    rain = "".join([k for k in rain if k not in special_chars]) # Delete special characters


    return [year, month, rain]


def file_to_df(filepath):
    '''Turn text file into pandas df.'''

    # Identify location
    location = filepath.split('/')[-1].split('.')[0]

    with open(filepath,'rt',encoding='utf-8') as file:
        lines = file.readlines()[2:]

        # Create empty final df
        result = pd.DataFrame(index=range(0, len(lines)), columns=['year','month','rain_mm'])

        # Iterate over lines of text
        for i, line in enumerate(lines):

            # Generate list of values and append it to df
            to_append = extract_values(line)
            result.iloc[i] = to_append

    # Format data type
    result.year = result.year.astype(int)
    result.month = result.month.astype(int)
    result.rain_mm = result.rain_mm.astype(float)

    # Add timestamp
    result['timestamp'] = result.apply(lambda row: datetime.strptime(f"{int(row.year)}-{int(row.month)}-15", '%Y-%m-%d'), axis=1)
    result['location'] = location
    result = result[['timestamp','year','month','location','rain_mm']]

    return result


# Set root dir
root = os.path.abspath(os.path.join("__file__", "../../"))

# Read data
# Cleaned
cambridge = file_to_df(filepath = root + '/data/raw/Cambridge.txt')
eastbourne = file_to_df(filepath = root + '/data/raw/Eastbourne.txt')
heathrow = file_to_df(filepath = root + '/data/raw/Heathrow.txt')
lowestoft = file_to_df(filepath = root + '/data/raw/Lowestoft.txt')
manston = file_to_df(filepath = root + '/data/raw/Manston.txt')
oxford = file_to_df(filepath = root + '/data/raw/Oxford.txt')

# Dump data
cambridge.to_csv(root + '/data/clean/cambridge.csv')
eastbourne.to_csv(root + '/data/clean/eastbourne.csv')
heathrow.to_csv(root + '/data/clean/heathrow.csv')
lowestoft.to_csv(root + '/data/clean/lowestoft.csv')
manston.to_csv(root + '/data/clean/manston.csv')
oxford.to_csv(root + '/data/clean/oxford.csv')
