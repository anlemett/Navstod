import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
import math

DATA_DIR = "Data"


sec_in_ms=0.000001
timeIntervalDuration = 180 #sec

def getTimeInterval(ms_num):
    
    ti = math.ceil(ms_num*sec_in_ms/timeIntervalDuration)
    ti = 1 if ti == 0 else ti
    return ti

#for corrupted file
def getTimeIntervalFromIndex(idx):
    
    ti = math.ceil((idx/50)/timeIntervalDuration)
    ti = 1 if ti == 0 else ti
    return ti



def add_run(df, filename, date, run):
    
    run_df = pd.read_csv(filename, sep=' ', dtype= {'date': str})
    
    run_df = run_df[run_df.Sensor == 'Eye Tracker']
    run_df = run_df[run_df["Eye movement type"] != 'EyesNotFound']
    
    no_rows = len(run_df.index)
    run_df['date'] = [date]*no_rows
    run_df['run']= [run]*no_rows
    
    if date == "230517" and run == 3:
        
        run_df['index1'] = run_df.index
        run_df['timeInterval'] = run_df.apply(lambda row: getTimeIntervalFromIndex(row['index1']), axis=1)
        run_df = run_df.drop('index1', axis=1)
    else:
        run_df['timeInterval'] = run_df.apply(lambda row: getTimeInterval(row['Computer timestamp']), axis=1)
    run_df = run_df[['date', 'run', 'timeInterval',
                     'Pupil diameter filtered', 
                     'Pupil diameter left', 
                     'Pupil diameter right', 
                     'Gaze event duration', 'Eye movement type']]
    
    timeIntervals = set(run_df['timeInterval'].tolist())
    print(timeIntervals)
    
    df = pd.concat([df, run_df])
    return df

df = pd.DataFrame()

full_filename = os.path.join(DATA_DIR, "230324_run1.csv")
df = add_run(df, full_filename, "230324", 1)

full_filename = os.path.join(DATA_DIR, "230324_run2.csv")
df = add_run(df, full_filename, "230324", 2)

full_filename = os.path.join(DATA_DIR, "230517_run1.csv")
df = add_run(df, full_filename, "230517", 1)

full_filename = os.path.join(DATA_DIR, "230517_run2.csv")
df = add_run(df, full_filename, "230517", 2)

full_filename = os.path.join(DATA_DIR, "230517_run3.csv")
df = add_run(df, full_filename, "230517", 3)

full_filename = os.path.join(DATA_DIR, "231115_run1.csv")
df = add_run(df, full_filename, "231115", 1)

full_filename = os.path.join(DATA_DIR, "231115_run2.csv")
df = add_run(df, full_filename, "231115", 2)

full_filename = os.path.join(DATA_DIR, "231115_run3.csv")
df = add_run(df, full_filename, "231115", 3)

full_filename = os.path.join(DATA_DIR, "231115_run4.csv")
df = add_run(df, full_filename, "231115", 4)

full_filename = os.path.join(DATA_DIR, "eye_tracking_all.csv")
df.to_csv(full_filename, sep= ' ', header=True, index=False)
