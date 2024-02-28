import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
import math

DATA_DIR = os.path.join("..", "..")
DATA_DIR_230324 = os.path.join(DATA_DIR, "230324")
DATA_DIR_230517 = os.path.join(DATA_DIR, "230517")
DATA_DIR_231115 = os.path.join(DATA_DIR, "231115")
OUTPUT_DIR = "Data"

#TODO: synchronize time of the 1st slot with CH data

sec_in_ms=0.000001
timeIntervalDuration = 180 #sec

def getTimeInterval(ms_num):

    return math.ceil(ms_num*sec_in_ms/timeIntervalDuration)


def add_run(df, filename, date, run):
    
    run_df = pd.read_excel(filename)
    
    run_df = run_df[run_df.Sensor == 'Eye Tracker']
    run_df = run_df[run_df["Eye movement type"] != 'EyesNotFound']
    
    no_rows = len(run_df.index)
    run_df['date'] = [date]*no_rows
    run_df['run']= [run]*no_rows
    
    run_df['timeInterval'] = run_df.apply(lambda row: getTimeInterval(row['Computer timestamp']), axis=1)
    run_df = run_df[['date', 'run', 'timeInterval',
                     'Pupil diameter filtered', 
                     'Gaze event duration', 'Eye movement type']]
    df = pd.concat([df, run_df])
    return df

df = pd.DataFrame()

full_filename = os.path.join(DATA_DIR_230324, "Run_1_attention.xlsx")
df = add_run(df, full_filename, "230324", 1)

full_filename = os.path.join(DATA_DIR_230324, "Run_2_attention.xlsx")
df = add_run(df, full_filename, "230324", 2)

full_filename = os.path.join(DATA_DIR_230517, "20230517T074332Z.xlsx")
df = add_run(df, full_filename, "230517", 1)

full_filename = os.path.join(DATA_DIR_230517, "20230517T084019Z.xlsx")
df = add_run(df, full_filename, "230517", 2)

full_filename = os.path.join(DATA_DIR_230517, "20230517T100316Z.xlsx")
df = add_run(df, full_filename, "230517", 3)

full_filename = os.path.join(DATA_DIR_231115, "Recording53.xlsx")
df = add_run(df, full_filename, "231115", 1)

full_filename = os.path.join(DATA_DIR_231115, "Recording54.xlsx")
df = add_run(df, full_filename, "231115", 2)

full_filename = os.path.join(DATA_DIR_231115, "Recording55.xlsx")
df = add_run(df, full_filename, "231115", 3)

full_filename = os.path.join(DATA_DIR_231115, "Recording56.xlsx")
df = add_run(df, full_filename, "231115", 4)

full_filename = os.path.join(OUTPUT_DIR, "eye_tracking_all.csv")
df.to_csv(full_filename, sep= ' ', header=True, index=False)
