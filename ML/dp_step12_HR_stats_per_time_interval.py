import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
from statistics import mean, median, stdev
from itertools import groupby

DATA_DIR = "Data"

def get_stats(lst):
    mean_lst = mean(lst) if lst else 0
    median_lst = median(lst) if lst else 0
    std_lst = stdev(lst) if (lst and len(lst)>1) else 0
    min_lst = min(lst) if lst else 0
    max_lst = max(lst) if lst else 0
    
    return (mean_lst, median_lst, std_lst, min_lst, max_lst)


def add_run_stats(new_df, run_df):
    
    date = run_df['date'].tolist()[0]
    run = run_df['run'].tolist()[0]
    
    num_time_intervals = len(set(run_df['timeInterval'].tolist()))
    
    for ti in range (1, num_time_intervals + 1):
        ti_df = run_df[run_df['timeInterval']==ti]
        
        # HR
        interval_HR = list(ti_df['HR'].dropna())
    
        (mean_HR, median_HR, std_HR,
         min_HR, max_HR) = get_stats(interval_HR)
        
        new_df = pd.concat([new_df, pd.DataFrame({
                            'date': [date],
                            'run': [run],
                            'timeInterval': [ti],
                            'mean_HR': [mean_HR],
                            'median_HR': [median_HR],
                            'std_HR': [std_HR],
                            'min_HR': [min_HR],
                            'max_HR': [max_HR],
                            })])
    
    return new_df


new_df = pd.DataFrame()

full_filename = os.path.join(DATA_DIR, "HR_all_norm.csv")

df = pd.read_csv(full_filename, sep= ' ', dtype={"date":str})

date_df = df[df.date == "230324"]

run_df = date_df[date_df.run == 1]
new_df = add_run_stats(new_df, run_df)

run_df = date_df[date_df.run == 2]
new_df = add_run_stats(new_df, run_df)

date_df = df[df.date == "230517"]

run_df = date_df[date_df.run == 1]
new_df = add_run_stats(new_df, run_df)

run_df = date_df[date_df.run == 2]
new_df = add_run_stats(new_df, run_df)

run_df = date_df[date_df.run == 3]
new_df = add_run_stats(new_df, run_df)

date_df = df[df.date == "231115"]

run_df = date_df[date_df.run == 1]
new_df = add_run_stats(new_df, run_df)

run_df = date_df[date_df.run == 2]
new_df = add_run_stats(new_df, run_df)

run_df = date_df[date_df.run == 3]
new_df = add_run_stats(new_df, run_df)

run_df = date_df[date_df.run == 4]
new_df = add_run_stats(new_df, run_df)


new_df.to_csv(os.path.join(DATA_DIR, "HR_stats_per_slot_norm.csv"), sep=' ',
            encoding='utf-8', float_format='%.8f', index = False, header = True)   
