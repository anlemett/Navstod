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

def add_run(df, filename, run):
    
    run_df = pd.read_csv(filename, sep=' ')
    
    num_slots = len(run_df.index)
    
    slot_lst = range(1, num_slots+1)
    run_df['timeInterval'] = slot_lst
    
    run_lst = [run]*num_slots
    run_df['run'] = run_lst
    
    run_df = run_df[['date', 'run', 'timeInterval', 'com_duration']]
    
    df = pd.concat([df, run_df])
    return df


df = pd.DataFrame(columns=['date', 'run', 'timeInterval',
                           'com_duration'])

full_filename = os.path.join(DATA_DIR_230324, "com_duration_230324_run1.csv")
df = add_run(df, full_filename, 1)

full_filename = os.path.join(DATA_DIR_230324, "com_duration_230324_run2.csv")
df = add_run(df, full_filename, 2)

full_filename = os.path.join(DATA_DIR_230517, "com_duration_230517_run1.csv")
df = add_run(df, full_filename, 1)

full_filename = os.path.join(OUTPUT_DIR, "com_duration_all.csv")
df.to_csv(full_filename, sep= ' ', header=True, index=False)