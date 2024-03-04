import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd

DATA_DIR = "Data"

def normilize(min, max, value):
    return ((value-min)/(max-min))


full_filename = os.path.join(DATA_DIR, "com_duration_all.csv")
df = pd.read_csv(full_filename, sep= ' ', dtype={'date':str})

new_df = pd.DataFrame()
'''
runs_dict = {
    "230324": [1,2],     # Fredrik
    "230517": [1,2,3],   # Fredrik
    "231115": [1,2,3,4], # Per, Christian, Dan, Fredrik
    }
'''

def addPilot(new_df, df):

    com_duration_min = df["com_duration"].min()
    com_duration_max = df["com_duration"].max()

    df['com_duration'] = df.apply(lambda row: normilize(com_duration_min, com_duration_max,
                                                 row['com_duration']), axis=1)

    new_df = pd.concat([new_df, df])
    
    return new_df


date_df = df[df['date']=="231115"]

# Fredrik
Fredrik_df = df[df['date']=="230324"]
date_df = df[df['date']=="230517"]
Fredrik_df = pd.concat([Fredrik_df, date_df])

new_df = addPilot(new_df, Fredrik_df)

new_df = new_df[['date', 'run', 'timeInterval', 'com_duration']]

full_filename = os.path.join(DATA_DIR, "com_duration_all_norm.csv")
new_df.to_csv(full_filename, sep= ' ', header=True, index=False)