import warnings
warnings.filterwarnings('ignore')

import os

import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIRS = [
    ('Pilots', os.path.abspath(os.path.join(BASE_DIR, '..', '..', '260129', 'Pilots'))),
    ('Bridge', os.path.abspath(os.path.join(BASE_DIR, '..', '..', '260129', 'Bridge'))),
]


def suffix_after_prefix(filename, prefix):
    stem = os.path.splitext(filename)[0]
    return stem.replace(prefix, '', 1)


def process_dataset(dataset_name, data_dir):
    if not os.path.isdir(data_dir):
        print(f'[{dataset_name}] Directory not found, skipping: {data_dir}')
        return 0

    av_files = sorted(
        name for name in os.listdir(data_dir)
        if name.lower().startswith('av_metrics_run') and name.lower().endswith('.csv')
    )
    wl_files = sorted(
        name for name in os.listdir(data_dir)
        if name.lower().startswith('wl_run') and name.lower().endswith('.csv')
    )

    if not av_files:
        print(f"[{dataset_name}] No files starting with 'av_metrics_run' found.")
        return 0
    if not wl_files:
        print(f"[{dataset_name}] No files starting with 'WL_run' found.")
        return 0

    wl_by_suffix = {
        suffix_after_prefix(name, 'WL_').lower(): name
        for name in wl_files
    }

    processed = 0
    for av_name in av_files:
        run_suffix = suffix_after_prefix(av_name, 'av_metrics_')
        wl_name = wl_by_suffix.get(run_suffix.lower())

        if wl_name is None:
            print(f'[{dataset_name}] Skipping {av_name}: no matching WL file for {run_suffix}')
            continue

        av_path = os.path.join(data_dir, av_name)
        wl_path = os.path.join(data_dir, wl_name)

        et_df = pd.read_csv(av_path, sep=' ', dtype={'date': str})
        ch_df = pd.read_csv(wl_path, sep=' ', dtype={'date': str})

        ch_df = ch_df.copy()
        ch_df['timeInterval'] = range(1, len(ch_df) + 1)

        run_df = pd.merge(et_df, ch_df, how='inner', on=['date', 'timeInterval'])

        out_name = f'ET_CH_{run_suffix}.csv'
        out_path = os.path.join(data_dir, out_name)
        run_df.to_csv(out_path, sep=' ', encoding='utf-8', float_format='%.8f', index=False, header=True)

        processed += 1
        print(f'[{dataset_name}] Processed {av_name} + {wl_name} -> {out_name}')

    return processed


def main():
    print(os.getcwd())

    total_processed = 0
    for dataset_name, data_dir in DATASET_DIRS:
        total_processed += process_dataset(dataset_name, data_dir)

    print(f'Total processed runs: {total_processed}')


if __name__ == '__main__':
    main()
