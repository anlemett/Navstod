import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd

DATA_DIR = "Data"

et_ch_df = pd.read_csv(os.path.join(DATA_DIR, "ML_ET_CH_norm.csv"), sep=' ',
                        dtype={'date':str})

HR_df = pd.read_csv(os.path.join(DATA_DIR, "HR_stats_per_slot_norm.csv"), sep=' ', dtype={'date':str})


new_df = pd.DataFrame()

runs_dict = {
    "230324": [1,2],
    "230517": [1,2,3],
    "231115": [1,2,3,4],
    }

for key in runs_dict:

    et_ch_date_df = et_ch_df[et_ch_df['date']==key]
    HR_date_df = HR_df[HR_df['date']==key]
       
    runs = runs_dict[key]
    
    for run in runs:
        
        et_ch_run_df = et_ch_date_df[et_ch_date_df['run']==run]
        HR_run_df = HR_date_df[HR_date_df['run']==run]
        
        run_df = pd.merge(et_ch_run_df, HR_run_df, how="inner", on=["date", "run", "timeInterval"])
                                  
        new_df = pd.concat([new_df, run_df])


new_df.to_csv(os.path.join(DATA_DIR, "ML_ET_HR_CH_norm.csv"), sep=' ', encoding='utf-8',
              float_format='%.8f', index = False, header = True)
