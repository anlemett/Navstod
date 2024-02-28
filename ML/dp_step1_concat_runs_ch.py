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
    
    run_df = run_df[['date', 'run', 'timeInterval', 'score', 'post_op_score']]
    
    df = pd.concat([df, run_df])
    return df


df = pd.DataFrame(columns=['date', 'run', 'timeInterval',
                           'score', 'post_op_score'])

full_filename = os.path.join(DATA_DIR_230324, "Wl1_Friedrik_230324_093826.csv")
df = add_run(df, full_filename, 1)

full_filename = os.path.join(DATA_DIR_230324, "Wl2_Fredrik_230324_112649.csv")
df = add_run(df, full_filename, 2)

full_filename = os.path.join(DATA_DIR_230517, "Exp1_Fredrick_230517_084542.csv")
df = add_run(df, full_filename, 1)

full_filename = os.path.join(DATA_DIR_230517, "Exp2_Fredrick2_230517_094640.csv")
df = add_run(df, full_filename, 2)

full_filename = os.path.join(DATA_DIR_230517, "Exp3_Fredrick_230517_111130.csv")
df = add_run(df, full_filename, 3)

full_filename = os.path.join(DATA_DIR_231115, "Run1_ pilot_Per_231115_103813.csv")
df = add_run(df, full_filename, 1)

full_filename = os.path.join(DATA_DIR_231115, "Run2_pilot_Christian_Schale_231115_125516.csv")
df = add_run(df, full_filename, 2)

full_filename = os.path.join(DATA_DIR_231115, "Run3_pilot_Dan_Krabbe_231115_140800.csv")
df = add_run(df, full_filename, 3)

full_filename = os.path.join(DATA_DIR_231115, "Run4_pilot_Fredrik_231115_151734.csv")
df = add_run(df, full_filename, 4)

full_filename = os.path.join(OUTPUT_DIR, "ch_all.csv")
df.to_csv(full_filename, sep= ' ', header=True, index=False)
