import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd

DATA_DIR = os.path.join("..", "..")
DATA_DIR = os.path.join(DATA_DIR, "240514_15")

day = 1
run_num = 1
glass_num = 2

#May 14
#Run 1 10:50 - 11:36 IMG 0006 Rickard 1 Anders E 1

filename = "av_metrics_d" + str(day) + "_r" + str(run_num) + "_g" + str(glass_num) + ".csv"

full_filename = os.path.join(DATA_DIR, filename)

et_df = pd.read_csv(full_filename, sep=' ',
                        dtype={'date':str})

filename = "scores_d" + str(day) + "_r" + str(run_num) + "_g" + str(glass_num) + ".csv"

full_filename = os.path.join(DATA_DIR, filename)

ch_df = pd.read_csv(full_filename, sep=' ', dtype={'date':str})

l = len(ch_df)
lst = range(1, l+1)
ch_df['timeInterval'] = lst

#ch_df['timeInterval'] -= 1
#ch_df = ch_df[ch_df.timeInterval>0]


new_df = pd.DataFrame()

run_df = pd.merge(et_df, ch_df, how="inner", on=["date", "timeInterval"])
                          
new_df = pd.concat([new_df, run_df])

filename = "ET_CH_d" + str(day) + "_r" + str(run_num) + "_g" + str(glass_num) + ".csv"
full_filename = os.path.join(DATA_DIR, filename)

new_df.to_csv(full_filename, sep=' ', encoding='utf-8',
              float_format='%.8f', index = False, header = True)