import numpy as np
from sklearn import metrics

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

if __name__ == '__main__':
    df2 = np.loadtxt('../data/data.csv', delimiter=',')
    X = df2[:, 0:3]
    X2 = df2[:, 3:-1]
    y = df2[:, -1]

    sc = StandardScaler()
    X = sc.fit_transform(X)
    X = np.hstack((X, X2))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)
    clf = RandomForestClassifier(max_depth=4, random_state=0)
    clf.fit(X_train, y_train)

    predictions = clf.predict(X_test)
    accuracy = metrics.accuracy_score(predictions, y_test)
    print('Accuracy:{0}%'.format(accuracy))
