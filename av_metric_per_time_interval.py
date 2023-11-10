import warnings
warnings.filterwarnings('ignore')

import os

#date = "230324"
date = "230517"
DATA_DIR = os.path.join("..", date)

import pandas as pd
import numpy as np
import math
from statistics import mean
import matplotlib.pyplot as plt
from itertools import groupby

run_num = 3
#filename = "Run_1_attention.xlsx"
if date == "230324":
    filename = "Run_" + str(run_num) +"_attention.xlsx"
elif date == "230517":
    if run_num == 1:
        filename = "20230517T074332Z.xlsx"
    elif run_num == 2:
        filename = "20230517T084019Z.xlsx"
    else:
        filename = "20230517T100316Z.xlsx"

output_filename = "av_metrics_" + date + "_run" + str(run_num) + ".csv"

full_filename = os.path.join(DATA_DIR, filename)

            
#new_df_inside_TMA = flight_df.loc[flight_df.index.get_level_values('sequence') >= first_point_index]
            
#new_df_inside_TMA.reset_index(drop=False, inplace=True)
        
df = pd.read_excel(full_filename)
print(df.head(1))

sec_in_ms=0.000001
timeIntervalDuration = 180 #sec

#def roundDownToNearest10(num):
#    return math.floor(num / 10) * 10

def getTimeInterval(ms_num):

    return math.ceil(ms_num*sec_in_ms/timeIntervalDuration)

df['timeInterval'] = df.apply(lambda row: getTimeInterval(row['Computer timestamp']), axis=1)

df = df[['Computer timestamp', 'timeInterval', 'Pupil diameter filtered', 'Gaze event duration',
         'Eye movement type']]

#print(df.head(5))


last_timestamp = list(df['Computer timestamp'])[-1]
print(last_timestamp)
last_timeinterval = getTimeInterval(last_timestamp)
print(last_timeinterval)

new_df = pd.DataFrame(columns=['timeInterval', 'av_pup_diameter', 'av_fixation',
                               'pup_diameter', 'fixation', 'number_of_sac', 'av_sac_duration'])
for ti in range (1, last_timeinterval + 1):
    ti_df = df[df['timeInterval']==ti]
    #print(ti_df.head(1))
    
    fixation_df = ti_df[ti_df['Eye movement type']=='Fixation']
    
    #interval_gaze = list(ti_df['Gaze event duration'].dropna())
    #interval_fixation = list(fixation_df['Gaze event duration'].dropna())
    lst = list(fixation_df['Gaze event duration'].dropna())

    # removing consecutive duplicates
    interval_fixation = [i[0] for i in groupby(lst)]
    
    av_fixation = mean(interval_fixation) if interval_fixation else 0
    fixation = interval_fixation[-1] if interval_fixation else 0
    interval_pup_diam = list(ti_df['Pupil diameter filtered'].dropna())
    av_diam = mean(interval_pup_diam) if interval_pup_diam else 0
    diam = interval_pup_diam[-1] if interval_pup_diam else 0
    #print(ti, av_gaze)
    
    if 'Saccade' in set(ti_df['Eye movement type']):
        saccades_df = ti_df[ti_df['Eye movement type']=='Saccade']
        lst = list(saccades_df['Gaze event duration'].dropna())
        # removing consecutive duplicates
        saccades_list = [i[0] for i in groupby(lst)]
        #print(saccades_list)
        #print(mean(saccades_list))
        #print(sum(saccades_list))
        #print(len(saccades_list))
        num_saccades = len(saccades_list)
        av_saccade_duration = mean(saccades_list) if saccades_list else 0
        #num_saccades = ti_df['Eye movement type'].value_counts()['Saccade']
    else:
        num_saccades = 0

    new_df = pd.concat([new_df, pd.DataFrame({'timeInterval': [ti],
                            'av_pup_diameter': [av_diam],
                            'pup_diameter': [diam],
                            'av_fixation': [av_fixation], 
                            'fixation': [fixation],
                            'number_of_sac': [num_saccades],
                            'av_sac_duration': [av_saccade_duration]
                            })])
    
new_df.to_csv(os.path.join(DATA_DIR, output_filename), sep=' ', encoding='utf-8', float_format='%.3f', index = False, header = True)   
print("stop")