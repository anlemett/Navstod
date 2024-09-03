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

sec_in_ms=0.000001
timeIntervalDuration = 180 #sec

#TODO: change to second?
def getMinute(ms_num):

    return math.ceil((ms_num*sec_in_ms)/60)

def synchTime(df, num_of_minutes):
    first_timestamp = df[df.minute>num_of_minutes]['Computer timestamp'].tolist()[0]
    
    df['Computer timestamp'] -= first_timestamp
    
    return df[df.minute>num_of_minutes]

# 230324 Run 1
full_filename = os.path.join(DATA_DIR_230324, "Run_1_attention.xlsx")
df = pd.read_excel(full_filename)

df['minute'] = df.apply(lambda row: getMinute(row['Computer timestamp']), axis=1)
df = synchTime(df, 4)
df = df.drop(columns=['minute'])
df.to_csv(os.path.join(OUTPUT_DIR, "230324_run1.csv"), sep=' ', header=True, index=False)

# 230324 Run 2
full_filename = os.path.join(DATA_DIR_230324, "Run_2_attention.xlsx")
df = pd.read_excel(full_filename)
df.to_csv(os.path.join(OUTPUT_DIR, "230324_run2.csv"), sep=' ', header=True, index=False)

# 230517 Run 1
full_filename = os.path.join(DATA_DIR_230517, "20230517T074332Z.xlsx")
df = pd.read_excel(full_filename)

df['minute'] = df.apply(lambda row: getMinute(row['Computer timestamp']), axis=1)
df = synchTime(df, 2)
df = df.drop(columns=['minute'])
df.to_csv(os.path.join(OUTPUT_DIR, "230517_run1.csv"), sep=' ', header=True, index=False)

# 230517 Run 2
full_filename = os.path.join(DATA_DIR_230517, "20230517T084019Z.xlsx")
df = pd.read_excel(full_filename)

df['minute'] = df.apply(lambda row: getMinute(row['Computer timestamp']), axis=1)
df = synchTime(df, 6)
df = df.drop(columns=['minute'])
df.to_csv(os.path.join(OUTPUT_DIR, "230517_run2.csv"), sep=' ', header=True, index=False)

# 230517 Run 3
full_filename = os.path.join(DATA_DIR_230517, "20230517T100316Z.xlsx")
df = pd.read_excel(full_filename)

df['minute'] = df.apply(lambda row: getMinute(row['Computer timestamp']), axis=1)
df = synchTime(df, 8)
df = df.drop(columns=['minute'])
df.to_csv(os.path.join(OUTPUT_DIR, "230517_run3.csv"), sep=' ', header=True, index=False)

# 231115 Run 1
full_filename = os.path.join(DATA_DIR_231115, "Recording53.xlsx")
df = pd.read_excel(full_filename)

df['minute'] = df.apply(lambda row: getMinute(row['Computer timestamp']), axis=1)
df = synchTime(df, 11)
df = df.drop(columns=['minute'])
df.to_csv(os.path.join(OUTPUT_DIR, "231115_run1.csv"), sep=' ', header=True, index=False)

# 231115 Run 2
full_filename = os.path.join(DATA_DIR_231115, "Recording54.xlsx")
df = pd.read_excel(full_filename)

df['minute'] = df.apply(lambda row: getMinute(row['Computer timestamp']), axis=1)
df = synchTime(df, 1)
df = df.drop(columns=['minute'])
df.to_csv(os.path.join(OUTPUT_DIR, "231115_run2.csv"), sep=' ', header=True, index=False)

# 231115 Run 3
full_filename = os.path.join(DATA_DIR_231115, "Recording55.xlsx")
df = pd.read_excel(full_filename)

df['minute'] = df.apply(lambda row: getMinute(row['Computer timestamp']), axis=1)
df = synchTime(df, 2)
df = df.drop(columns=['minute'])
df.to_csv(os.path.join(OUTPUT_DIR, "231115_run3.csv"), sep=' ', header=True, index=False)

# 231115 Run 4
full_filename = os.path.join(DATA_DIR_231115, "Recording56.xlsx")
df = pd.read_excel(full_filename)
df.to_csv(os.path.join(OUTPUT_DIR, "231115_run4.csv"), sep=' ', header=True, index=False)
