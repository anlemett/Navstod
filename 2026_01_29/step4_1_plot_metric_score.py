import warnings
warnings.filterwarnings('ignore')

import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIRS = [
    ('Pilots', os.path.abspath(os.path.join(BASE_DIR, '..', '..', '260129', 'Pilots'))),
    ('Bridge', os.path.abspath(os.path.join(BASE_DIR, '..', '..', '260129', 'Bridge'))),
]
FIG_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'Figures'))

POST_OP = False
METRICS = ['av_sac_duration', 'number_of_sac', 'av_fixation', 'av_pup_diameter']


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def list_et_ch_files(data_dir):
    if not os.path.isdir(data_dir):
        return []
    files = []
    for name in os.listdir(data_dir):
        if name.lower().startswith('et_ch_run') and name.lower().endswith('.csv'):
            files.append(os.path.join(data_dir, name))
    return sorted(files)


def metric_label(metric):
    if metric == 'av_fixation':
        return 'av. fixation [ms]'
    if metric == 'av_pup_diameter':
        return 'av. pup. diameter [mm]'
    if metric == 'number_of_sac':
        return '# saccades'
    return 'av. sac. duration [ms]'


def plot_file(full_filename, dataset_name):
    filename = os.path.basename(full_filename)
    run_suffix = os.path.splitext(filename)[0].replace('ET_CH_', '', 1)

    df = pd.read_csv(full_filename, sep=' ', dtype={'date': str, 'score': int, 'post_op_score': int})

    time_intervals_all = list(df['timeInterval'])
    scores_col = 'post_op_score' if POST_OP else 'score'
    scores_all = list(df[scores_col])

    if len(scores_all) > len(time_intervals_all):
        scores_all = scores_all[:len(time_intervals_all)]

    number_of_points = len(scores_all)
    time_intervals = time_intervals_all[:number_of_points]

    for metric in METRICS:
        metric_lst = list(df[metric])[:number_of_points]

        plt.clf()
        ax1 = plt.subplot(1, 1, 1)
        ax2 = ax1.twinx()

        ax1.yaxis.get_major_locator().set_params(integer=True)

        score_label = 'post op scores' if POST_OP else 'scores'
        lns1 = ax1.plot(time_intervals, scores_all, color='r', label=score_label)
        lns2 = ax2.plot(time_intervals, metric_lst, color='g', label=metric, linestyle='dashed')

        for t in ax1.get_yticklabels():
            t.set_color('r')
        for t in ax2.get_yticklabels():
            t.set_color('g')

        ax2.set_xticks(np.arange(1, number_of_points + 1, 1))
        lns = lns1 + lns2
        ax2.legend(lns, ['scores', metric_label(metric)], loc='best')

        out_name = f'ET_CH_{run_suffix}_post_op_{metric}.png' if POST_OP else f'ET_CH_{run_suffix}_{metric}.png'
        run_dir = os.path.join(FIG_DIR, '260129', dataset_name, run_suffix, metric)
        ensure_dir(run_dir)

        out_path = os.path.join(run_dir, out_name)
        plt.savefig(out_path)

    print(f'[{dataset_name}] Plotted: {filename} ({number_of_points} points)')


def main():
    print(os.getcwd())
    ensure_dir(FIG_DIR)

    total_plotted = 0
    for dataset_name, data_dir in DATASET_DIRS:
        et_ch_files = list_et_ch_files(data_dir)
        if not et_ch_files:
            print(f"[{dataset_name}] No files starting with 'ET_CH_run' found.")
            continue

        for path in et_ch_files:
            plot_file(path, dataset_name)
        total_plotted += len(et_ch_files)

    print(f'Total plotted files: {total_plotted}')


if __name__ == '__main__':
    main()
