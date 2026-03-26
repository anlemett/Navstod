import warnings
warnings.filterwarnings('ignore')

import os

DATA_DIR = os.path.joinDATA_DIR = os.path.join("..", "..", "251029")
print(os.getcwd())
if os.path.isdir(DATA_DIR):
    print("Directory exists")
else:
    print("Directory does not exist")

import pandas as pd
import math
from statistics import mean
from itertools import groupby

date = '251029'
run_num = 8

filename = "ET_synch_run" + str(run_num) + ".csv"

output_filename = "av_metrics_run" + str(run_num) + ".csv"

full_filename = os.path.join(DATA_DIR, filename)

df = pd.read_csv(full_filename, sep=' ')

# cut off time before the run starts
time_to_cut = 0

sec_in_ms=0.000001
timeIntervalDuration = 180 #sec

def getTimeInterval(ms_num):

    return math.ceil(ms_num*sec_in_ms/timeIntervalDuration)

df['timeInterval'] = df.apply(lambda row: getTimeInterval(row['Computer timestamp']), axis=1)

df = df[['Computer timestamp', 'timeInterval', 'Pupil diameter filtered', 'Eye movement event duration',
         'Eye movement type']]


last_timestamp = list(df['Computer timestamp'])[-1]
print(last_timestamp)
last_timeinterval = getTimeInterval(last_timestamp)
print(last_timeinterval)

new_df = pd.DataFrame(columns=['date', 'timeInterval', 'av_pup_diameter', 'av_fixation',
                               'pup_diameter', 'fixation', 'number_of_sac', 'av_sac_duration'])

for ti in range (1, last_timeinterval + 1):
    ti_df = df[df['timeInterval']==ti]
    #print(ti_df.head(1))
    
    fixation_df = ti_df[ti_df['Eye movement type']=='Fixation']
    
    lst = list(fixation_df['Eye movement event duration'].dropna())

    # removing consecutive duplicates
    interval_fixation = [i[0] for i in groupby(lst)]
    
    av_fixation = mean(interval_fixation) if interval_fixation else 0
    fixation = interval_fixation[-1] if interval_fixation else 0
    interval_pup_diam = list(ti_df['Pupil diameter filtered'].dropna())
    av_diam = mean(interval_pup_diam) if interval_pup_diam else 0
    diam = interval_pup_diam[-1] if interval_pup_diam else 0
    
    if 'Saccade' in set(ti_df['Eye movement type']):

        saccades_df = ti_df[ti_df['Eye movement type']=='Saccade']
        lst = list(saccades_df['Eye movement event duration'].dropna())

        # removing consecutive duplicates
        saccades_list = [i[0] for i in groupby(lst)]

        num_saccades = len(saccades_list)
        av_saccade_duration = mean(saccades_list) if saccades_list else 0

    else:
        num_saccades = 0

    new_df = pd.concat([new_df, pd.DataFrame({
                            'date': [date],
                            'timeInterval': [ti],
                            'av_pup_diameter': [av_diam],
                            'pup_diameter': [diam],
                            'av_fixation': [av_fixation], 
                            'fixation': [fixation],
                            'number_of_sac': [num_saccades],
                            'av_sac_duration': [av_saccade_duration]
                            })])
    
new_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)   
