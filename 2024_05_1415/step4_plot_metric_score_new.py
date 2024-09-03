import warnings
warnings.filterwarnings('ignore')

import os

DATA_DIR = os.path.join("..", "..")
DATA_DIR = os.path.join(DATA_DIR, "240514_15")
FIG_DIR = 'Figures'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

day = 1
run_num = 1
glass_num = 2

filename = "ET_CH_d" + str(day) + "_r" + str(run_num) + "_g" + str(glass_num) + ".csv"
full_filename = os.path.join(DATA_DIR, filename)

df = pd.read_csv(full_filename, sep=' ', dtype={'date':str, 'score':int, 
                                                    })
#score_df['score'] = score_df['score'].replace([0], 10)

metrics = ['av_sac_duration', 'number_of_sac', 'av_fixation', 'av_pup_diameter']

for metric in metrics:
            
    metric_lst = list(df[metric])
        
    time_intervals = list(df['timeInterval'])

    scores = list(df['score'])
            
    intervals_num = len(time_intervals)

    if len(scores) > intervals_num:
        scores = scores[0:intervals_num]

    number_of_points = len(scores)
    print(number_of_points)

    time_intervals = time_intervals[0:number_of_points]
    metrics = metrics[0:number_of_points]
            
    plt.clf()
    ax1 = plt.subplot(1, 1, 1)
    ax2 = ax1.twinx()

    ax1.yaxis.get_major_locator().set_params(integer=True)

    lns1 = ax1.plot(time_intervals, scores, color='r', label='scores')

    lns2 = ax2.plot(time_intervals, metric_lst, color='g', label=metric,
                                linestyle='dashed')

    for t in ax1.get_yticklabels():
        t.set_color('r')
        
    for t in ax2.get_yticklabels():
        t.set_color('g')
  
    ax2.set_xticks(np.arange(1, number_of_points+1, 1))
            
    # Adding legend
    lns = lns1 +  lns2
    if metric == 'av_fixation':
        metric_legend = 'av. fixation [ms]'
    elif metric == 'av_pup_diameter':
        metric_legend = 'av. pup. diameter [mm]'
    elif metric == 'number_of_sac':
        metric_legend = '# saccades'
    elif metric == 'av_sac_duration':
        metric_legend = 'av. sac. duration [ms]'

    ax2.legend(lns, ["scores", metric_legend], loc='best')

    filename = "ET_CH_d" + str(day) + "_r" + str(run_num) + "_g" + str(glass_num) + "_" + metric + '.png'
    
    subdir = "d" + str(day) + "_r" + str(run_num) + "_g" + str(glass_num)
            
    dir = os.path.join(FIG_DIR, subdir)
    if not os.path.exists(dir):
        os.mkdir(dir)
    dir = os.path.join(dir, metric)
    if not os.path.exists(dir):
        os.mkdir(dir)
    full_filename = os.path.join(dir,filename)
    plt.savefig(full_filename)



