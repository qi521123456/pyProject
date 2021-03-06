import test_abalone as abaData

import numpy as np

X,y=abaData.getData()
X_train, X_test, y_train, y_test = abaData.train_test(X, y, 0.2)

def NB():
    from sklearn.naive_bayes import GaussianNB
    clf = GaussianNB().fit(X_train, y_train)
    predict = clf.predict(X_test)
    return predict

def dt():
    from sklearn import tree
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train,y_train)
    predict = clf.predict(X_test)
    return predict

def svm():
    from sklearn import svm
    clf = svm.SVC()
    clf.fit(X_train,y_train)
    predict = clf.predict(X_test)
    return predict

predict = svm()
a = 0
b = 0
for i, j in enumerate(predict):
    if int(j) == y_test[i]:
        a += 1
    else:
        b += 1

print(a, b)

# X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
# Y = np.array([1, 1, 1, 2, 2, 2])
# clf = GaussianNB().fit(X, Y)
# print(clf.predict([[-0.8,-1]]) )