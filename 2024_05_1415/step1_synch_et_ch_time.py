import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
import math

DATA_DIR = os.path.join("..", "..")
DATA_DIR = os.path.join(DATA_DIR, "240514_15")

sec_in_ms=0.000001
timeIntervalDuration = 180 #sec

def getSecond(ms_num):

    return math.ceil(ms_num*sec_in_ms)

def synchTime(df, num_of_seconds):
    first_timestamp = df[df.second>num_of_seconds]['Computer timestamp'].tolist()[0]
    
    df['Computer timestamp'] -= first_timestamp
    
    return df[df.second>num_of_seconds]

day = 1
run_num = 1
glass_num = 2
num_of_sec = 0

#May 14
#Run 1 10:50 - 11:36 IMG 0006 Rickard 1 Anders E 1

filename = "ET_d" + str(day) + "_r" + str(run_num) + "_g" + str(glass_num) + ".xlsx"

output_filename = "ET_d" + str(day) + "_r" + str(run_num) + "_g" + str(glass_num) + ".csv"

full_filename = os.path.join(DATA_DIR, filename)

full_output_filename = os.path.join(DATA_DIR, output_filename)

df = pd.read_excel(full_filename)

df['second'] = df.apply(lambda row: getSecond(row['Computer timestamp']), axis=1)
df = synchTime(df, num_of_sec)
df = df.drop(columns=['second'])
df.to_csv(full_output_filename, sep=' ', header=True, index=False)
