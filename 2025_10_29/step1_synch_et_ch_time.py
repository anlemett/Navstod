import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
import math

run_num = 8

DATA_DIR = os.path.joinDATA_DIR = os.path.join("..", "..", "251029")
print(os.getcwd())
if os.path.isdir(DATA_DIR):
    print("Directory exists")
else:
    print("Directory does not exist")

sec_in_ms=0.000001
timeIntervalDuration = 180 #sec

def getSecond(ms_num):

    return math.ceil(ms_num*sec_in_ms)

def synchTime(df, num_of_seconds):
    first_timestamp = df[df.second>num_of_seconds]['Computer timestamp'].tolist()[0]
    
    df['Computer timestamp'] -= first_timestamp
    
    return df[df.second>num_of_seconds]


if (run_num == 1):
    num_of_sec = 132
elif (run_num == 2):
    num_of_sec = 167
elif (run_num == 4):
    num_of_sec = 55
elif (run_num == 8):
    num_of_sec = 99
else:
    num_of_sec = 0



filename = "ET_run" + str(run_num) + ".xlsx"

output_filename = "ET_synch_run" + str(run_num) + ".csv"

full_filename = os.path.join(DATA_DIR, filename)

full_output_filename = os.path.join(DATA_DIR, output_filename)

df = pd.read_excel(full_filename)

df['second'] = df.apply(lambda row: getSecond(row['Computer timestamp']), axis=1)
df = synchTime(df, num_of_sec)
df = df.drop(columns=['second'])
df.to_csv(full_output_filename, sep=' ', header=True, index=False)
