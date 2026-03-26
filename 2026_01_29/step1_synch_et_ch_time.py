import warnings
warnings.filterwarnings('ignore')

import os
import re
from datetime import datetime, timedelta

import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIRS = [
    ('Pilots', os.path.abspath(os.path.join(BASE_DIR, '..', '..', '260129', 'Pilots'))),
    ('Bridge', os.path.abspath(os.path.join(BASE_DIR, '..', '..', '260129', 'Bridge'))),
]


def parse_hhmmss(value):
    s = str(value).strip()
    if '.' in s:
        s = s.split('.')[0]
    s = s.zfill(6)
    return datetime.strptime(s, '%H%M%S').time()


def is_hhmmss_like(value):
    try:
        parse_hhmmss(value)
        return True
    except (TypeError, ValueError):
        return False


def parse_start_datetime(value):
    if pd.isna(value):
        raise ValueError('Missing Recording start time in ET file.')
    ts = pd.to_datetime(value, dayfirst=True, errors='coerce')
    if pd.isna(ts):
        ts = pd.to_datetime(value, dayfirst=False, errors='coerce')
    if pd.isna(ts):
        raise ValueError(f'Cannot parse Recording start time: {value}')
    return ts


def find_recording_timestamp_column(et_df):
    for col in ['Recording timestamp', 'Recording time stamp']:
        if col in et_df.columns:
            return col
    raise KeyError("Neither 'Recording timestamp' nor 'Recording time stamp' found in ET file.")


def synchronize_et_to_wl(et_df, wl_df):
    if 'Recording start time' not in et_df.columns:
        raise KeyError("Column 'Recording start time' not found in ET file.")

    ts_col = find_recording_timestamp_column(et_df)

    wl_time_column = None
    if 'time' in wl_df.columns:
        time_values = wl_df['time'].dropna()
        if not time_values.empty and is_hhmmss_like(time_values.iloc[0]):
            wl_time_column = 'time'

    if wl_time_column is None:
        for col in wl_df.columns:
            val_series = wl_df[col].dropna()
            if val_series.empty:
                continue
            if is_hhmmss_like(val_series.iloc[0]):
                wl_time_column = col
                break

    if wl_time_column is None:
        raise KeyError('Could not find WL time column (expected hhmmss values).')

    wl_start_time = parse_hhmmss(wl_df[wl_time_column].dropna().iloc[0])
    et_start_dt = parse_start_datetime(et_df['Recording start time'].iloc[0])
    wl_start_dt = et_start_dt.replace(
        hour=wl_start_time.hour,
        minute=wl_start_time.minute,
        second=wl_start_time.second,
        microsecond=0,
    )

    if wl_start_dt < et_start_dt:
        wl_start_dt = wl_start_dt + timedelta(days=1)

    et_abs_time = et_start_dt + pd.to_timedelta(et_df[ts_col], unit='ms')
    return et_df.loc[et_abs_time >= wl_start_dt].copy()


def run_key_from_name(filename, prefix):
    stem = os.path.splitext(filename)[0]
    suffix = stem[len(prefix):]
    return suffix.lower()


def list_prefixed_files(directory, pattern, extension):
    results = []
    regex = re.compile(pattern, flags=re.IGNORECASE)
    for name in os.listdir(directory):
        if not name.lower().endswith(extension.lower()):
            continue
        if regex.match(name):
            results.append(name)
    return sorted(results)


def process_dataset(dataset_name, data_dir):
    if not os.path.isdir(data_dir):
        print(f'[{dataset_name}] Directory not found, skipping: {data_dir}')
        return 0

    et_files = list_prefixed_files(data_dir, r'^ET_run', '.xlsx')
    wl_files = list_prefixed_files(data_dir, r'^WL_\s*run', '.csv')

    if not et_files:
        print(f"[{dataset_name}] No ET files found starting with 'ET_run'.")
        return 0
    if not wl_files:
        print(f"[{dataset_name}] No WL files found starting with 'WL_ run' or 'WL_run'.")
        return 0

    wl_by_key = {}
    for wl_name in wl_files:
        key = run_key_from_name(wl_name, 'WL_')
        wl_by_key[key] = wl_name

    processed = 0
    for et_name in et_files:
        et_key = run_key_from_name(et_name, 'ET_')
        wl_name = wl_by_key.get(et_key)

        if wl_name is None:
            print(f'[{dataset_name}] Skipping {et_name}: no matching WL file for key {et_key}')
            continue

        et_path = os.path.join(data_dir, et_name)
        wl_path = os.path.join(data_dir, wl_name)

        et_df = pd.read_excel(et_path)
        wl_df = pd.read_csv(wl_path, sep=' ', dtype={'date': str})

        synced_et_df = synchronize_et_to_wl(et_df, wl_df)

        out_stem = os.path.splitext(et_name)[0].replace('ET_', 'ET_synch_', 1)
        out_path = os.path.join(data_dir, out_stem + '.csv')
        synced_et_df.to_csv(out_path, sep=' ', header=True, index=False)

        processed += 1
        print(f'[{dataset_name}] Processed {et_name} + {wl_name} -> {os.path.basename(out_path)}')

    return processed


def main():
    print(os.getcwd())

    total_processed = 0
    for dataset_name, data_dir in DATASET_DIRS:
        total_processed += process_dataset(dataset_name, data_dir)

    print(f'Total processed pairs: {total_processed}')


if __name__ == '__main__':
    main()
