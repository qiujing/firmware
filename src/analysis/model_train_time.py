import time

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

dataset1 = pd.read_csv(r'../data/DataSet2.csv')
X1 = dataset1.iloc[:, :13].values
Y1 = dataset1.iloc[:, 13].values

RF_train = []
RF_test = []
for test_size in range(10, 95, 5):
    best = 0
    time_all_train = 0
    time_all_test = 0
    test_size = 100 - test_size
    for i in range(50):
        # Splitting the dataset into the Training set and Test set
        X_train, X_test, Y_train, Y_test = train_test_split(X1, Y1, test_size=test_size / 100, random_state=0)
        # Feature Scaling
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        classifier = RandomForestClassifier(criterion='entropy', min_samples_leaf=2, class_weight='balanced')
        # train
        train_time_start = time.time()
        classifier.fit(X_train, Y_train)
        train_time_end = time.time()
        train_time = train_time_end - train_time_start
        time_all_train += train_time
        # predict
        test_time_start = time.time()
        predict_results = classifier.predict(X_test)
        test_time_end = time.time()
        test_time = test_time_end - test_time_start
        time_all_test += test_time

        result = accuracy_score(predict_results, Y_test)
        if best < result:
            best = result
    RF_train.append(time_all_train / 50)
    RF_test.append(time_all_test / 50)
    print(best)
    # print(time_all_train/50)
    # print(time_all_test/50)

dataset2 = pd.read_csv(r'../data/DataSet5.csv')
X2 = dataset2.iloc[:, :13].values
Y2 = dataset2.iloc[:, 13].values

Decision_train = []
Decision_test = []
for test_size in range(10, 95, 5):
    best = 0
    time_all_train = 0
    time_all_test = 0
    test_size = 100 - test_size
    for i in range(50):
        # Splitting the dataset into the Training set and Test set
        X_train, X_test, Y_train, Y_test = train_test_split(X2, Y2, test_size=test_size / 100, random_state=0)
        # Feature Scaling
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
        # train
        train_time_start = time.time()
        classifier.fit(X_train, Y_train)
        train_time_end = time.time()
        train_time = train_time_end - train_time_start
        time_all_train += train_time
        # predict
        test_time_start = time.time()
        predict_results = classifier.predict(X_test)
        test_time_end = time.time()
        test_time = test_time_end - test_time_start
        time_all_test += test_time
        result = accuracy_score(predict_results, Y_test)
        # print(result)
        if best < result:
            best = result
    Decision_train.append(time_all_train / 50)
    Decision_test.append(time_all_test / 50)
    print(best)

xgboost_train = []
xgboost_test = []
for test_size in range(10, 95, 5):
    # Splitting the dataset into the Training set and Test set
    best = 0
    time_all_train = 0
    time_all_test = 0
    test_size = 100 - test_size
    for i in range(50):
        X_train, X_test, Y_train, Y_test = train_test_split(X2, Y2, test_size=test_size / 100, random_state=0)
        # Feature Scaling
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        classifier = XGBClassifier(booster='gbtree', random_state=27)
        train_time_start = time.time()
        classifier.fit(X_train, Y_train)
        train_time_end = time.time()
        train_time = train_time_end - train_time_start
        time_all_train += train_time
        # predict
        test_time_start = time.time()
        predict_results = classifier.predict(X_test)
        test_time_end = time.time()
        test_time = test_time_end - test_time_start
        time_all_test += test_time
        result = accuracy_score(predict_results, Y_test)
        if best < result:
            best = result
    xgboost_train.append(time_all_train / 50)
    xgboost_test.append(time_all_test / 50)
    print(best)

file = open(r'Time_WithString_DecisionTree_Test.txt', 'w')
for i in Decision_test:
    file.write(str(i) + ' ')
file.close()
file = open(r'Time_WithString_RF_Test.txt', 'w')
for i in RF_test:
    file.write(str(i) + ' ')
file.close()
file = open(r'Time_WithString_XGBoost_Test.txt', 'w')
for i in xgboost_test:
    file.write(str(i) + ' ')
file.close()

file = open(r'Time_WithString_DecisionTree_Train.txt', 'w')
for i in Decision_train:
    file.write(str(i) + ' ')
file.close()
file = open(r'Time_WithString_RF_Train.txt', 'w')
for i in RF_train:
    file.write(str(i) + ' ')
file.close()
file = open(r'Time_WithString_XGBoost_Train.txt', 'w')
for i in xgboost_train:
    file.write(str(i) + ' ')
file.close()
