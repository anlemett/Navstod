import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd

DATA_DIR = "Data"

def normilize(min, max, value):
    return ((value-min)/(max-min))

def normilize_saccade_fixation(sac_min, sac_max, fix_min, fix_max, 
                               value, event):
    if event == "Saccade":
        return ((value-sac_min)/(sac_max-sac_min))
    elif event == "Fixation":
        return ((value-fix_min)/(fix_max-fix_min))
    else: # "Unclassified"
        return value


full_filename = os.path.join(DATA_DIR, "eye_tracking_all.csv")
df = pd.read_csv(full_filename, sep= ' ', dtype={'date':str})

new_df = pd.DataFrame()
'''
runs_dict = {
    "230324": [1,2],     # Fredrik
    "230517": [1,2,3],   # Fredrik
    "231115": [1,2,3,4], # Per, Christian, Dan, Fredrik
    }
'''

def addPilot(new_df, df):

    pup_diam_min = df["Pupil diameter filtered"].min()
    pup_diam_max = df["Pupil diameter filtered"].max()

    df['Pupil_diameter_filtered'] = df.apply(lambda row: normilize(pup_diam_min, pup_diam_max,
                                                 row['Pupil diameter filtered']), axis=1)

    saccade_df = df[df["Eye movement type"]=='Saccade']
    fixation_df = df[df["Eye movement type"]=='Fixation']

    saccade_min = saccade_df["Gaze event duration"].min()
    saccade_max = saccade_df["Gaze event duration"].max()

    fixation_min = fixation_df["Gaze event duration"].min()
    fixation_max = fixation_df["Gaze event duration"].max()

    df['Gaze_event_duration'] = df.apply(lambda row: normilize_saccade_fixation(
                                    saccade_min, saccade_max, fixation_min, fixation_max,
                                    row['Gaze event duration'],
                                    row['Eye movement type'],
                                    ), axis=1)

    new_df = pd.concat([new_df, df])
    
    return new_df


date_df = df[df['date']=="231115"]

# Per
run_df = date_df[date_df.run==1]
new_df = addPilot(new_df, run_df)

# Christian
run_df = date_df[date_df.run==2]
new_df = addPilot(new_df, run_df)

# Dan
run_df = date_df[date_df.run==3]
new_df = addPilot(new_df, run_df)

# Fredrik
Fredrik_df = date_df[date_df.run==4]
date_df = df[df['date']=="230324"]
Fredrik_df = pd.concat([Fredrik_df, date_df])
date_df = df[df['date']=="230517"]
Fredrik_df = pd.concat([Fredrik_df, date_df])

new_df = addPilot(new_df, Fredrik_df)

new_df = new_df[['date', 'run', 'timeInterval', 'Pupil_diameter_filtered', 
                 'Gaze_event_duration', 'Eye movement type']]

full_filename = os.path.join(DATA_DIR, "eye_tracking_all_norm.csv")
new_df.to_csv(full_filename, sep= ' ', header=True, index=False)