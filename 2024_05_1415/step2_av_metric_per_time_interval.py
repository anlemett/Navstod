import warnings
warnings.filterwarnings('ignore')

import os

DATA_DIR = os.path.join("..", "..")
DATA_DIR = os.path.join(DATA_DIR, "240514_15")

import pandas as pd
import math
from statistics import mean
from itertools import groupby

day = 1
run_num = 1
glass_num = 2

#May 14
#Run 1 10:50 - 11:36 IMG 0006 Rickard 1 Anders E 1

filename = "ET_d" + str(day) + "_r" + str(run_num) + "_g" + str(glass_num) + ".csv"

output_filename = "av_metrics" + "_d" + str(day) + "_r" + str(run_num) + "_g" + str(glass_num) + ".csv"

full_filename = os.path.join(DATA_DIR, filename)

df = pd.read_csv(full_filename, sep=' ')

# cut off time before the run starts
time_to_cut = 0

sec_in_ms=0.000001
timeIntervalDuration = 180 #sec

def getTimeInterval(ms_num):

    return math.ceil(ms_num*sec_in_ms/timeIntervalDuration)

df['timeInterval'] = df.apply(lambda row: getTimeInterval(row['Computer timestamp']), axis=1)

df = df[['Computer timestamp', 'timeInterval', 'Pupil diameter filtered', 'Gaze event duration',
         'Eye movement type']]


last_timestamp = list(df['Computer timestamp'])[-1]
print(last_timestamp)
last_timeinterval = getTimeInterval(last_timestamp)
print(last_timeinterval)

new_df = pd.DataFrame(columns=['date', 'timeInterval', 'av_pup_diameter', 'av_fixation',
                               'pup_diameter', 'fixation', 'number_of_sac', 'av_sac_duration'])

date = '240514'

for ti in range (1, last_timeinterval + 1):
    ti_df = df[df['timeInterval']==ti]
    #print(ti_df.head(1))
    
    fixation_df = ti_df[ti_df['Eye movement type']=='Fixation']
    
    lst = list(fixation_df['Gaze event duration'].dropna())

    # removing consecutive duplicates
    interval_fixation = [i[0] for i in groupby(lst)]
    
    av_fixation = mean(interval_fixation) if interval_fixation else 0
    fixation = interval_fixation[-1] if interval_fixation else 0
    interval_pup_diam = list(ti_df['Pupil diameter filtered'].dropna())
    av_diam = mean(interval_pup_diam) if interval_pup_diam else 0
    diam = interval_pup_diam[-1] if interval_pup_diam else 0
    
    if 'Saccade' in set(ti_df['Eye movement type']):

        saccades_df = ti_df[ti_df['Eye movement type']=='Saccade']
        lst = list(saccades_df['Gaze event duration'].dropna())

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
