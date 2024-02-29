import warnings
warnings.filterwarnings('ignore')

import os

DATA_DIR = os.path.join("ML", "Data")
FIG_DIR = 'Figures'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

filename = "ML_ET_CH.csv"
full_filename = os.path.join(DATA_DIR, filename)

full_df = pd.read_csv(full_filename, sep=' ', dtype={'date':str, 'score':int, 
                                                      'post_op_score':int})
#score_df['score'] = score_df['score'].replace([0], 10)

runs_dict = {
    "230324": [1,2],     # Fredrik
    "230517": [1,2,3],   # Fredrik
    "231115": [1,2,3,4], # Per, Christian, Dan, Fredrik
    }

metrics = ['mean_sac_duration', 'number_of_sac', 'mean_fixation', 'mean_pup_diam']


post_ops = [True, False]

for key in runs_dict:
    
    date_df = full_df[full_df['date']==key]
    
    for run in runs_dict[key]:
        run_df = date_df[date_df.run==run]
                
        for metric in metrics:
            
            metric_lst = list(run_df[metric])
        
            time_intervals = list(run_df['timeInterval'])

            scores = list(run_df['score'])
            
            if key!= "230324":
                scores_post_op = list(run_df['post_op_score'])

            intervals_num = len(time_intervals)

            if len(scores) > intervals_num:
                scores = scores[0:intervals_num]
                if key!= "230324":
                    scores_post_op = scores_post_op[0:intervals_num]

            number_of_points = len(scores)
            print(number_of_points)

            time_intervals = time_intervals[0:number_of_points]
            metrics = metrics[0:number_of_points]
            
            for post_op in post_ops:
                
                if post_op:
                    if key == "230324":
                        continue
                
                plt.clf()
                ax1 = plt.subplot(1, 1, 1)
                ax2 = ax1.twinx()

                ax1.yaxis.get_major_locator().set_params(integer=True)

                if post_op:
                    lns1 = ax1.plot(time_intervals, scores_post_op, color='b',
                                        label='scores post op')
                else:
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
                if metric == 'mean_fixation':
                    metric_legend = 'av. fixation [ms]'
                elif metric == 'mean_pup_diam':
                    metric_legend = 'av. pup. diameter [mm]'
                elif metric == 'number_of_sac':
                    metric_legend = '# saccades'
                elif metric == 'mean_sac_duration':
                    metric_legend = 'av. sac. duration [ms]'

                if post_op:
                    ax2.legend(lns, ["scores post op",metric_legend], loc='best')
                else:
                    ax2.legend(lns, ["scores",metric_legend], loc='best')
            
                if post_op:
                    filename = key + '_run' + str(run) + '_' + metric + '_post_op.png'
                else:
                    filename = key + '_run' + str(run) + '_' + metric + '.png'
                dir = os.path.join(FIG_DIR, key)
                if not os.path.exists(dir):
                    os.mkdir(dir)
                dir = os.path.join(dir, metric)
                if not os.path.exists(dir):
                    os.mkdir(dir)
                full_filename = os.path.join(dir,filename)
                plt.savefig(full_filename)



