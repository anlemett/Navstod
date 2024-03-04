import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
from statistics import mean, median, stdev
from itertools import groupby

DATA_DIR = "Data"

NORMALIZED = True
#NORMALIZED = False

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
        if NORMALIZED:
            lst = list(saccades_df['Gaze_event_duration'].dropna())
        else:
            lst = list(saccades_df['Gaze event duration'].dropna())
    
        # removing consecutive duplicates
        saccades_list = [i[0] for i in groupby(lst)]

        num_saccades = len(saccades_list) if saccades_list else 0
        total_sac_duration = sum(saccades_list) if saccades_list else 0
    
        (mean_sac_duration, median_sac_duration, std_sac_duration,
         min_sac_duration, max_sac_duration) = get_stats(saccades_list)

        # Fixation duration
        
        fixation_df = ti_df[ti_df['Eye movement type']=='Fixation']
        if NORMALIZED:
            lst = list(fixation_df['Gaze_event_duration'].dropna())
        else:
            lst = list(fixation_df['Gaze event duration'].dropna())
    
        # removing consecutive duplicates
        interval_fixation = [i[0] for i in groupby(lst)]
    
        (mean_fix_duration, median_fix_duration, std_fix_duration,
         min_fix_duration, max_fix_duration) = get_stats(interval_fixation)
            
        # Pupil diameter
        if NORMALIZED:
            interval_pup_diam = list(ti_df['Pupil_diameter_filtered'].dropna())
            interval_pup_diam_left = list(ti_df['Pupil_diameter_left'].dropna())
            interval_pup_diam_right = list(ti_df['Pupil_diameter_right'].dropna())
        else:
            interval_pup_diam = list(ti_df['Pupil diameter filtered'].dropna())
            interval_pup_diam_left = list(ti_df['Pupil diameter left'].dropna())
            interval_pup_diam_right = list(ti_df['Pupil diameter right'].dropna())
    
        (mean_pup_diam, median_pup_diam, std_pup_diam,
         min_pup_diam, max_pup_diam) = get_stats(interval_pup_diam)
        
        (mean_pup_diam_left, median_pup_diam_left, std_pup_diam_left,
         min_pup_diam_left, max_pup_diam_left) = get_stats(interval_pup_diam_left)
        
        (mean_pup_diam_right, median_pup_diam_right, std_pup_diam_right,
         min_pup_diam_right, max_pup_diam_right) = get_stats(interval_pup_diam_right)
        
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
                            'mean_pup_diam_left': [mean_pup_diam_left],
                            'median_pup_diam_left': [median_pup_diam_left],
                            'std_pup_diam_left': [std_pup_diam_left],
                            'min_pup_diam_left': [min_pup_diam_left],
                            'max_pup_diam_left': [max_pup_diam_left],
                            'mean_pup_diam_right': [mean_pup_diam_right],
                            'median_pup_diam_right': [median_pup_diam_right],
                            'std_pup_diam_right': [std_pup_diam_right],
                            'min_pup_diam_right': [min_pup_diam_right],
                            'max_pup_diam_right': [max_pup_diam_right],
                            })])
    
    return new_df


new_df = pd.DataFrame()
if NORMALIZED:
    full_filename = os.path.join(DATA_DIR, "eye_tracking_all_norm.csv")
else:
    full_filename = os.path.join(DATA_DIR, "eye_tracking_all.csv")
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

if NORMALIZED:
    new_df.to_csv(os.path.join(DATA_DIR, "et_stats_per_slot_norm.csv"), sep=' ',
            encoding='utf-8', float_format='%.8f', index = False, header = True)   
else:
    new_df.to_csv(os.path.join(DATA_DIR, "et_stats_per_slot.csv"), sep=' ',
            encoding='utf-8', float_format='%.8f', index = False, header = True)   
    