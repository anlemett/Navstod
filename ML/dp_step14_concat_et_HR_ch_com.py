import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd

DATA_DIR = "Data"

et_hr_ch_df = pd.read_csv(os.path.join(DATA_DIR, "ML_ET_HR_CH_norm.csv"), sep=' ',
                    dtype={'date':str})
    
com_df = pd.read_csv(os.path.join(DATA_DIR, "com_duration_all_norm.csv"), sep=' ', dtype={'date':str})


new_df = pd.DataFrame()

runs_dict = {
    "230324": [1,2],
    "230517": [1] #[1,2,3],
    #"231115": [1,2,3,4],
    }

for key in runs_dict:

    et_hr_ch_date_df = et_hr_ch_df[et_hr_ch_df['date']==key]
    com_date_df = com_df[com_df['date']==key]
       
    runs = runs_dict[key]
    
    for run in runs:
        
        et_hr_ch_run_df = et_hr_ch_date_df[et_hr_ch_date_df['run']==run]
        com_run_df = com_date_df[com_date_df['run']==run]
        
        run_df = pd.merge(et_hr_ch_run_df, com_run_df, how="inner", on=["date", "run", "timeInterval"])
                          
        new_df = pd.concat([new_df, run_df])


new_df.to_csv(os.path.join(DATA_DIR, "ML_ET_HR_COM_CH_norm.csv"), sep=' ', encoding='utf-8',
        float_format='%.8f', index = False, header = True)
