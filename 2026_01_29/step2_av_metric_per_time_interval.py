import warnings
warnings.filterwarnings('ignore')

import os
import math
from statistics import mean
from itertools import groupby

import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIRS = [
    ('Pilots', os.path.abspath(os.path.join(BASE_DIR, '..', '..', '260129', 'Pilots'))),
    ('Bridge', os.path.abspath(os.path.join(BASE_DIR, '..', '..', '260129', 'Bridge'))),
]
DATE_VALUE = '260129'

sec_in_ms = 0.000001
timeIntervalDuration = 180  # sec


def getTimeInterval(ms_num):
    return math.ceil(ms_num * sec_in_ms / timeIntervalDuration)


def process_et_synch_file(input_path, output_dir, dataset_name):
    input_name = os.path.basename(input_path)
    run_suffix = os.path.splitext(input_name)[0].replace('ET_synch_', '', 1)
    output_name = f'av_metrics_{run_suffix}.csv'
    output_path = os.path.join(output_dir, output_name)

    df = pd.read_csv(input_path, sep=' ')
    df['timeInterval'] = df['Computer timestamp'].apply(getTimeInterval)

    df = df[[
        'Computer timestamp',
        'timeInterval',
        'Pupil diameter filtered',
        'Eye movement event duration',
        'Eye movement type',
    ]]

    last_timeinterval = int(df['timeInterval'].max())

    rows = []
    for ti in range(1, last_timeinterval + 1):
        ti_df = df[df['timeInterval'] == ti]

        fixation_df = ti_df[ti_df['Eye movement type'] == 'Fixation']
        fixation_list = [i[0] for i in groupby(list(fixation_df['Eye movement event duration'].dropna()))]

        av_fixation = mean(fixation_list) if fixation_list else 0
        fixation = fixation_list[-1] if fixation_list else 0

        interval_pup_diam = list(ti_df['Pupil diameter filtered'].dropna())
        av_diam = mean(interval_pup_diam) if interval_pup_diam else 0
        diam = interval_pup_diam[-1] if interval_pup_diam else 0

        num_saccades = 0
        av_saccade_duration = 0
        if 'Saccade' in set(ti_df['Eye movement type']):
            saccades_df = ti_df[ti_df['Eye movement type'] == 'Saccade']
            saccade_durations = list(saccades_df['Eye movement event duration'].dropna())
            saccades_list = [i[0] for i in groupby(saccade_durations)]

            num_saccades = len(saccades_list)
            av_saccade_duration = mean(saccades_list) if saccades_list else 0

        rows.append({
            'date': DATE_VALUE,
            'timeInterval': ti,
            'av_pup_diameter': av_diam,
            'pup_diameter': diam,
            'av_fixation': av_fixation,
            'fixation': fixation,
            'number_of_sac': num_saccades,
            'av_sac_duration': av_saccade_duration,
        })

    new_df = pd.DataFrame(rows)
    new_df.to_csv(output_path, sep=' ', encoding='utf-8', float_format='%.3f', index=False, header=True)
    print(f'[{dataset_name}] Processed {input_name} -> {output_name}')


def process_dataset(dataset_name, data_dir):
    if not os.path.isdir(data_dir):
        print(f'[{dataset_name}] Directory not found, skipping: {data_dir}')
        return 0

    input_files = sorted(
        name for name in os.listdir(data_dir)
        if name.lower().startswith('et_synch_run') and name.lower().endswith('.csv')
    )

    if not input_files:
        print(f"[{dataset_name}] No files starting with 'ET_synch_run' found.")
        return 0

    for name in input_files:
        process_et_synch_file(os.path.join(data_dir, name), data_dir, dataset_name)

    return len(input_files)


def main():
    print(os.getcwd())

    total_processed = 0
    for dataset_name, data_dir in DATASET_DIRS:
        total_processed += process_dataset(dataset_name, data_dir)

    print(f'Total processed files: {total_processed}')


if __name__ == '__main__':
    main()
