from sklearn.datasets import load_boston
import pandas as pd
import sklearn.model_selection
import os

boston = load_boston()

# Preparing and splitting the data
X = pd.DataFrame(boston.data, columns=boston.feature_names)
Y = pd.DataFrame(boston.target)


# split data into test, train, validation

# split train 0.66 and test 0.33
X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size = 0.33)


# split train into train and valid such that train = 0.66 * 0.66 , valid = 0.66 * 0.33
X_train, X_val, Y_train, Y_val = sklearn.model_selection.train_test_split(X_train, Y_train, test_size = 0.33)


# This is our local data directory. We need to make sure that it exists.

data_dir = '../data/boston'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# save test, train, val on csv file without header or index
    
X_test.to_csv(os.path.join(data_dir, 'test.csv'), header = False, index = False)

Y_test.to_csv(os.path.join(data_dir, 'GroundTruthTest.csv'), header = False, index = False)

pd.concat([Y_train, X_train], axis = 1).to_csv(os.path.join(data_dir, 'train.csv'), header = False, index = False)
pd.concat([Y_val, X_val], axis = 1).to_csv(os.path.join(data_dir, 'val.csv'), header = False, index = False)    


    