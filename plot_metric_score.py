import warnings
warnings.filterwarnings('ignore')

import os

#date = "230324"
#date = "230517"
date = "231115"
DATA_DIR = os.path.join("..", date)

import pandas as pd
import numpy as np
import math
from statistics import mean
import matplotlib.pyplot as plt

run_num = 1
post_op = False
#post_op = True

#filename = "av_metrics" + str(run_num) + ".csv"
filename = "av_metrics_" + date + "_run" + str(run_num) + ".csv"
        
full_filename = os.path.join(DATA_DIR, filename)

metric_df = pd.read_csv(full_filename, sep=' ')

#metric = 'av_fixation'
#metric = 'av_pup_diameter'
#metric = 'av_sac_duration'
metric = 'number_of_sac'

metrics = list(metric_df[metric])
#metrics.pop()
time_intervals = list(metric_df['timeInterval'])
#time_intervals.pop()

if date == "230324":
    if run_num == 1:
        filename = "Wl1_Fredrik_230324_093826.csv"
    else:
        filename = "Wl2_Fredrik_230324_112649.csv"
elif date == "230517":
    if run_num == 1:
        filename = "Exp1_Fredrick_230517_084542.csv"
    elif run_num == 2:
        filename = "Exp2_Fredrick2_230517_094640.csv"
    else:
        filename = "Exp3_Fredrick_230517_111130.csv"
elif date == "231115":
    if run_num == 1:
        filename = "Run1_ pilot_Per_231115_103813.csv"
    elif run_num == 2:
        filename = "Run2_pilot_Christian_Schale_231115_125516.csv"
    elif run_num == 3:
        filename = "Run3_pilot_Dan_Krabbe_231115_140800.csv"
    else:
        filename = "Run4_pilot_Fredrik_231115_151734.csv"

full_filename = os.path.join(DATA_DIR, filename)

score_df = pd.read_csv(full_filename, sep=' ',index_col=False)
score_df.score = score_df.score.astype(int)
score_df.post_op_score = score_df.post_op_score.astype(int)
#print(score_df.head(1))

#score_df['score'] = score_df['score'].replace([0], 10)

scores = list(score_df['score'])

if post_op:
    scores_post_op = list(score_df['post_op_score'])
    print(scores_post_op)

#print(len(scores))

intervals_num = len(time_intervals)
print(intervals_num)
if len(scores) > intervals_num:
    scores = scores[0:intervals_num]
    if post_op:
        scores_post_op = scores_post_op[0:intervals_num]

number_of_points = len(scores)

time_intervals = time_intervals[0:number_of_points]
metrics = metrics[0:number_of_points]

if post_op:
    print(scores_post_op)
else:
    print(scores)

ax1 = plt.subplot(1, 1, 1)
ax2 = ax1.twinx()

ax1.yaxis.get_major_locator().set_params(integer=True)

if post_op:
    lns1 = ax1.plot(time_intervals, scores_post_op, color='b',
                    label='scores post op')
else:
    lns1 = ax1.plot(time_intervals, scores, color='r', label='scores')

lns2 = ax2.plot(time_intervals, metrics, color='g', label=metric,
                linestyle='dashed')

for t in ax1.get_yticklabels():
    t.set_color('r')
        
for t in ax2.get_yticklabels():
    t.set_color('g')
  
# Naming the x-axis, y-axis and the whole graph
#ax2.xlabel("Time interval")

ax2.set_xticks(np.arange(1, number_of_points+1, 1))
  
# Adding legend, which helps us recognize the curve according to it's color
lns = lns1 +  lns2

if metric == 'av_fixation':
    metric_legend = 'av. fixation [ms]'
elif metric == 'av_pup_diameter':
    metric_legend = 'av. pup. diameter [mm]'
elif metric == 'number_of_sac':
    metric_legend = '# saccades'
elif metric == 'av_sac_duration':
    metric_legend = 'av. sac. duration [ms]'
    
if post_op:
    ax2.legend(lns, ["scores post op",metric_legend], loc='best')
else:
    ax2.legend(lns, ["scores",metric_legend], loc='best')

  
# To load the display window
plt.show()
