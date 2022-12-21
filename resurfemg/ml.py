"""
Copyright 2022 Netherlands eScience Center and University of Twente
Licensed under the Apache License, version 2.0. See LICENSE for details.

This file contains functions run machine learning algorithms on arrays
over them.
"""


# basic ds
import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# basic system
# import sys
import os
import glob

# math and signals
# import math
from scipy.stats import entropy
# from scipy.signal import savgol_filter
# from scipy.signal import find_peaks


# ml stuff
# import sklearn #?
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.svm import SVC
# # from sklearn.metrics import accuracy_score
# from sklearn.linear_model import LogisticRegression
# from sklearn import tree
# from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
from resurfemg import helper_functions as hf

# here we will import our models ,
# apply them over the arrays
# then output both the array and the decision array
# into a list


def save_ml_output(arrays, out_fname, force):
    """
    This function is written to be called by the cli module.
    It stores arrays in a directory.
    """
    if not force:
        if os.path.isfile(out_fname):
            return
    try:
        os.makedirs(os.path.dirname(out_fname))
    except FileExistsError:
        pass
    np.save(out_fname, arrays, allow_pickle=False)


def applu_model(arrays_folder, model_file, output_folder, features=['mean', 'entropy'] ):
    """
    This function applies an ML model over a bunch of arrays.
    """
    file_directory_list = glob.glob(
        os.path.join(arrays_folder, '**/*.npy'),
        recursive=True,
    )
    model = joblib.load(model_file)
    # arrays_and_pred = []
    for array in file_directory_list:
        array = np.load(array)
    index_ml_hold = []
    predictions_made = []
    holder = []
    sc = StandardScaler()
    if features == ['mean', 'entropy']
    
    for slice in hf.slices_jump_slider(array, 1000,1):
        mean_feature = slice.mean() #close to mean
        entropy_feature = entropy(slice)
        holder.append(slice)
        ml_index_test= [mean_feature, entropy_feature]

        index_ml_hold.append(ml_index_test)
        X_test_live = index_ml_hold
        X_test_live = sc.transform(X_test_live)
        y_pred = model.predict(X_test_live)
        array_and_pred = np.vstack(array, y_pred)

    # OK- then turn it into a 2 lead array, then save as below
    rel_fname = os.path.relpath(array, arrays_folder)
    out_fname = os.path.join(output_folder, rel_fname)
    save_ml_output(array_and_pred, out_fname)
