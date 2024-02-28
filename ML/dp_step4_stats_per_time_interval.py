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
    std_lst = stdev(lst) if lst else 0
    min_lst = min(lst) if lst else 0
    max_lst = max(lst) if lst else 0
    
    return (mean_lst, median_lst, std_lst, min_lst, max_lst)


def add_run_stats(new_df, run_df):
    
    date = run_df['date'].tolist()[0]
    run = run_df['run'].tolist()[0]
    
    num_time_intervals = len(set(run_df['timeInterval'].tolist()))
    
    for ti in range (1, num_time_intervals + 1):
        ti_df = run_df[run_df['timeInterval']==ti]
    
        # Saccades duration and number

        saccades_df = ti_df[ti_df['Eye movement type']=='Saccade']
        lst = list(saccades_df['Gaze_event_duration'].dropna())
    
        # removing consecutive duplicates
        saccades_list = [i[0] for i in groupby(lst)]

        num_saccades = len(saccades_list) if saccades_list else 0
        total_sac_duration = sum(saccades_list) if saccades_list else 0
    
        (mean_sac_duration, median_sac_duration, std_sac_duration,
         min_sac_duration, max_sac_duration) = get_stats(saccades_list)

        # Fixation duration
        
        fixation_df = ti_df[ti_df['Eye movement type']=='Fixation']
        lst = list(fixation_df['Gaze_event_duration'].dropna())
    
        # removing consecutive duplicates
        interval_fixation = [i[0] for i in groupby(lst)]
    
        (mean_fix_duration, median_fix_duration, std_fix_duration,
         min_fix_duration, max_fix_duration) = get_stats(interval_fixation)
            
        # Pupil diameter
    
        interval_pup_diam = list(ti_df['Pupil_diameter_filtered'].dropna())
    
        (mean_pup_diam, median_pup_diam, std_pup_diam,
         min_pup_diam, max_pup_diam) = get_stats(interval_pup_diam)
    
        new_df = pd.concat([new_df, pd.DataFrame({
                            'date': [date],
                            'run': [run],
                            'timeInterval': [ti],
                            'number_of_sac': [num_saccades],
                            'total_sac_duration': [total_sac_duration],
                            'mean_sac_duration': [mean_sac_duration],
                            'median_sac_duration': [median_sac_duration],
                            'std_sac_duration': [std_sac_duration],
                            'min_sac_duration': [min_sac_duration],
                            'max_sac_duration': [max_sac_duration],
                            'mean_fixation': [mean_fix_duration], 
                            'median_fixation': [median_fix_duration], 
                            'std_fixation': [std_fix_duration], 
                            'min_fixation': [min_fix_duration], 
                            'max_fixation': [max_fix_duration], 
                            'mean_pup_diam': [mean_pup_diam],
                            'median_pup_diam': [median_pup_diam],
                            'std_pup_diam': [std_pup_diam],
                            'min_pup_diam': [min_pup_diam],
                            'max_pup_diam': [max_pup_diam],
                            })])
    
    return new_df


new_df = pd.DataFrame()
full_filename = os.path.join(DATA_DIR, "eye_tracking_all_norm.csv")
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

new_df.to_csv(os.path.join(DATA_DIR, "et_stats_per_slot.csv"), sep=' ', encoding='utf-8',
              float_format='%.8f', index = False, header = True)   