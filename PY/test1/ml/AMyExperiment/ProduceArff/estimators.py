from NASAMDPSDPdata import AllData
from sklearn.model_selection import GridSearchCV
from sklearn import ensemble
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

def rf():
    from sklearn.ensemble import RandomForestClassifier

if __name__ == '__main__':
    pass