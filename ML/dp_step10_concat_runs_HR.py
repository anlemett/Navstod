import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
import math
import sys

DATA_DIR = os.path.join("..", "..")
OUTPUT_DIR = "Data"

sec_in_ms=0.000001
timeIntervalDuration = 3 #min

def getTimeInterval(time, start_time):
    
    minutes = int(time[3:5])
    start_minutes = int(start_time[3:5])
    if minutes < start_minutes:
        minutes = minutes + 60
    ti = math.floor((minutes-start_minutes)/timeIntervalDuration) + 1
    
    return ti

def add_run(df, filename, date, run):
    
    run_df = pd.read_csv(filename, sep=',', dtype={'time':str})
    
    no_rows = len(run_df.index)
    run_df['date'] = [date]*no_rows
    run_df['run']= [run]*no_rows
    
    start_time = run_df['Time'].tolist()[0]
    run_df['timeInterval'] = run_df.apply(lambda row: getTimeInterval(row['Time'], start_time),
                                          axis=1)
       
    run_df = run_df[['date', 'run', 'timeInterval', 'Heart Rate']]
    
    df = pd.concat([df, run_df])
    return df


df = pd.DataFrame(columns=['date', 'run', 'timeInterval', 'Heart Rate'])

runs_dict = {
    "230324": [1,2],     # Fredrik
    "230517": [1,2,3],   # Fredrik
    "231115": [1,2,3,4], # Per, Christian, Dan, Fredrik
    }


for key in runs_dict:
    DATE_DATA_DIR = os.path.join(DATA_DIR, key)
    
    for run in runs_dict[key]:
        full_filename = os.path.join(DATE_DATA_DIR,
                        "HR_" + key + "_run" + str(run) + ".csv")
        df = add_run(df, full_filename, key, run)


full_filename = os.path.join(OUTPUT_DIR, "HR_all.csv")
df.to_csv(full_filename, sep= ' ', header=True, index=False)