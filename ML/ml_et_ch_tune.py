import warnings
warnings.filterwarnings('ignore')

import time
import os
import numpy as np
import pandas as pd
import random
#import sys

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.svm import SVC

from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, train_test_split
from scipy.stats import randint

DATA_DIR = "Data"

#BINARY = True
BINARY = False

#POST_OP = True
POST_OP = False

features = [
            'number_of_sac', 'total_sac_duration',
            'mean_sac_duration', 'median_sac_duration', 'std_sac_duration',
            'min_sac_duration', 'max_sac_duration',
            'mean_fixation', 'median_fixation', 'std_fixation',
            'min_fixation', 'max_fixation',
            'mean_pup_diam_left', 'median_pup_diam_left', 'std_pup_diam_left',
            'min_pup_diam_left', 'max_pup_diam_left',
            'mean_pup_diam_right', 'median_pup_diam_right', 'std_pup_diam_right',
            'min_pup_diam_right', 'max_pup_diam_right'
            ]

df = pd.read_csv(os.path.join(DATA_DIR, "ML_ET_CH_norm.csv"), sep=' ', dtype={'date':str})

if POST_OP:
    df = df[df.date!="230324"]
    scores = df.post_op_score.tolist()
else:
    scores = df.score.tolist()
    
X_df = df[features]
    
if BINARY:
    scores = [1 if score < 4 else 2 for score in scores]
else:
    scores = [1 if score < 2 else 3 if score > 3 else 2 for score in scores]

#random.shuffle(scores)

# Spit the data into train and test
X_train_df, X_test_df, y_train, y_test = train_test_split(
    X_df, scores, test_size=0.1, shuffle=True, random_state=0
    )

clf = RandomForestClassifier(class_weight='balanced',
                             bootstrap=False,
                             max_features=None,
                             random_state=0)

# Use random search to find the best hyperparameters
param_dist = {'n_estimators': randint(50,500),
     'max_depth': randint(1,17),
     }

search = RandomizedSearchCV(clf, 
                            param_distributions = param_dist, 
                            n_iter=5, 
                            cv=10)

# Fit the search object to the data
search.fit(X_train_df, y_train)

# Create a variable for the best model
best_rf = search.best_estimator_

# Print the best hyperparameters
print('Best hyperparameters:',  search.best_params_)
#BINARY = True
#POST_OP = True
#test_size=0.1, shuffle=True, random_state=0 -> 'max_depth': 2, 'n_estimators': 245
#POST_OP = False
#test_size=0.1, shuffle=True, random_state=0 -> 'max_depth': 14, 'n_estimators': 369
#BINARY = False
#POST_OP = True
#test_size=0.1, shuffle=True, random_state=0 -> 'max_depth': 6, 'n_estimators': 482
#POST_OP = False
#test_size=0.1, shuffle=True, random_state=0 -> 'max_depth': 16, 'n_estimators': 134

y_pred = best_rf.predict(X_test_df)

print(y_test)
print(y_pred)

accuracy = accuracy_score(y_pred=y_pred, y_true=y_test)
if BINARY:
    precision = precision_score(y_pred=y_pred, y_true=y_test, average='binary')
    recall = recall_score(y_pred=y_pred, y_true=y_test, average='binary')
    f1 = f1_score(y_pred=y_pred, y_true=y_test, average='binary')
else:
    f1 = f1_score(y_pred=y_pred, y_true=y_test, average='micro')
    recall = recall_score(y_pred=y_pred, y_true=y_test, average='micro')
    precision = precision_score(y_pred=y_pred, y_true=y_test, average='micro')

print("Accuracy:", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1-score:", f1)
