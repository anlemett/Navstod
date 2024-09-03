import warnings
warnings.filterwarnings('ignore')

import time
import os
import numpy as np
import pandas as pd
from statistics import mean
#import sys

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.svm import SVC

from sklearn import model_selection
from sklearn.inspection import permutation_importance

DATA_DIR = "Data"

RANDOM_STATE = 0

BINARY = True
#BINARY = False

#POST_OP = True
POST_OP = False

FEATURE_IMPORTANCE = True
#FEATURE_IMPORTANCE = False

features = [
            'number_of_sac', 'total_sac_duration',
            'mean_sac_duration', 'median_sac_duration', 'std_sac_duration',
            'min_sac_duration', 'max_sac_duration',
            'mean_fixation', 'median_fixation', 'std_fixation',
            'min_fixation', 'max_fixation',
            'mean_pup_diam_left', 'median_pup_diam_left', 'std_pup_diam_left',
            'min_pup_diam_left', 'max_pup_diam_left',
            'mean_pup_diam_right', 'median_pup_diam_right', 'std_pup_diam_right',
            'min_pup_diam_right', 'max_pup_diam_right',
            #'mean_HR', 'median_HR', 'std_HR', 'min_HR', 'max_HR',
            'com_duration'
            ]

number_of_features = len(features)

#df = pd.read_csv(os.path.join(DATA_DIR, "ML_ET_CH_norm.csv"), sep=' ', dtype={'date':str})
#df = pd.read_csv(os.path.join(DATA_DIR, "ML_ET_HR_CH_norm.csv"), sep=' ', dtype={'date':str})
df = pd.read_csv(os.path.join(DATA_DIR, "ML_ET_CH_COM_norm.csv"), sep=' ', dtype={'date':str})
#df = pd.read_csv(os.path.join(DATA_DIR, "ML_ET_HR_COM_CH_norm.csv"), sep=' ', dtype={'date':str})

if POST_OP:
    df = df[df.date!="230324"]
    scores = df.post_op_score.tolist()
else:
    scores = df.score.tolist()

X_df = df[features]


if BINARY:
    scores = [1 if score < 4 else 2 for score in scores]
#else:
#    scores = [1 if score < 2 else 3 if score > 3 else 2 for score in scores]


# Define the K-fold Cross Validator
num_folds = 10
kfold = model_selection.KFold(n_splits=num_folds, shuffle=True, random_state=RANDOM_STATE)
    
# K-fold Cross Validation model evaluation
    
# Define per-fold score containers
acc_per_fold = []
prec_per_fold = []
rec_per_fold = []
f1_per_fold = []

if FEATURE_IMPORTANCE:
    gini_kfold_importances = np.empty(shape=[num_folds, number_of_features])
    perm_kfold_importances = np.empty(shape=[num_folds, number_of_features])
    
fold_no = 1
for train_idx, test_idx in kfold.split(scores):
    
    X_train = np.array(X_df)[train_idx.astype(int)]
    y_train = np.array(scores)[train_idx.astype(int)]
    X_test = np.array(X_df)[test_idx.astype(int)]
    y_test = np.array(scores)[test_idx.astype(int)]

    if POST_OP:
        if BINARY:
            #md = 9   #rs=0, good
            #ne = 330 
            md = 13
            ne = 97
        else:
            md = 6
            ne = 482
    else:
        if BINARY:
            md = 13
            ne = 97
        else:
            md = 16
            ne = 134
    
    clf = RandomForestClassifier(
        class_weight='balanced',
        bootstrap=False,
        max_features=None,
        max_depth=md,
        n_estimators=ne,
        random_state = RANDOM_STATE
        )

    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    
    if FEATURE_IMPORTANCE:
        gini_fold_importances = clf.feature_importances_
        gini_kfold_importances[fold_no-1, :] = gini_fold_importances
        
        perm_fold_importances = permutation_importance(
            clf, X_test, y_test, n_repeats=10, random_state= RANDOM_STATE, n_jobs=2
            )
        perm_kfold_importances[fold_no-1, :] = perm_fold_importances.importances_mean

    
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
    
    acc_per_fold.append(accuracy)
    prec_per_fold.append(precision)
    rec_per_fold.append(recall)
    f1_per_fold.append(f1)
    
    # Increase fold number
    fold_no = fold_no + 1

print(acc_per_fold)
print(prec_per_fold)
print(rec_per_fold)
print(f1_per_fold)

print(mean(acc_per_fold))
print(mean(f1_per_fold))

if FEATURE_IMPORTANCE:
    importances_mean = np.mean(gini_kfold_importances, axis=0)
       
    importances_df = pd.DataFrame()
    importances_df['feature'] = features
    importances_df['importance'] = importances_mean
   
    importances_df.sort_values(by=['importance'], ascending=False,inplace=True)
    importances_df.to_csv("forest_importances_gini.csv", sep=',', header=True, index=False)
       
    importances_mean = np.mean(perm_kfold_importances, axis=0)
      
    importances_df = pd.DataFrame()
    importances_df['feature'] = features
    importances_df['importance'] = importances_mean
   
    importances_df.sort_values(by=['importance'], ascending=False,inplace=True)
    importances_df.to_csv("forest_importances_perm.csv", sep=',', header=True, index=False)

