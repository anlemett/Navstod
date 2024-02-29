import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd

DATA_DIR = "Data"

NORMALIZED = True
#NORMALIZED = False

if NORMALIZED:
    et_df = pd.read_csv(os.path.join(DATA_DIR, "et_stats_per_slot_norm.csv"), sep=' ',
                        dtype={'date':str})
else:
    et_df = pd.read_csv(os.path.join(DATA_DIR, "et_stats_per_slot.csv"), sep=' ',
                        dtype={'date':str})

ch_df = pd.read_csv(os.path.join(DATA_DIR, "ch_all.csv"), sep=' ', dtype={'date':str})

new_df = pd.DataFrame()

runs_dict = {
    "230324": [1,2],
    "230517": [1,2,3],
    "231115": [1,2,3,4],
    }

for key in runs_dict:

    et_date_df = et_df[et_df['date']==key]
    ch_date_df = ch_df[ch_df['date']==key]
       
    runs = runs_dict[key]
    
    for run in runs:
        
        et_run_df = et_date_df[et_date_df['run']==run]
        ch_run_df = ch_date_df[ch_date_df['run']==run]
        
        run_df = pd.merge(et_run_df, ch_run_df, how="inner", on=["date", "run", "timeInterval"])
                          
        new_df = pd.concat([new_df, run_df])

if NORMALIZED:
    new_df.to_csv(os.path.join(DATA_DIR, "ML_ET_CH_norm.csv"), sep=' ', encoding='utf-8',
              float_format='%.8f', index = False, header = True)
else:
    new_df.to_csv(os.path.join(DATA_DIR, "ML_ET_CH.csv"), sep=' ', encoding='utf-8',
              float_format='%.8f', index = False, header = True)