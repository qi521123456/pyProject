from scipy.io import arff
import os
import numpy as np
from sklearn.model_selection import train_test_split,KFold
from sklearn.preprocessing import Normalizer
from sklearn.ensemble import IsolationForest,RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import auc,roc_curve
def processData(path):
    X = []
    y = []
    with open(path, 'r') as fr:
        data, meta = arff.loadarff(fr)
        for d in data:
            X.append(tuple(d)[:-1])  # 必须强转
            y.append(d[-1].decode())
    return np.log2(np.mat(X)+1),y

def bulidClassifier(X,y,algorithm,n):
    '''
    :param X:
    :param y:
    :param algorithm:
    :param n: n折交叉
    :return: 取n折后平均值
    '''
    # iforest = IsolationForest()
    X = np.array(X,dtype='float64')
    y = np.array(y)
    scaler = Normalizer()
    # trainX,testX,trainY,testY = train_test_split(X,y,test_size=0.2)
    cv = KFold(n)
    roc_auc_s = []
    for i, (train, test) in enumerate(cv.split(X, y)):
        trainX = X[train]
        testX = X[test]
        trainY = y[train]
        testY = y[test]
        if len(np.unique(testY))==1:
            continue
        trainX = scaler.fit_transform(trainX)
        testX = scaler.fit_transform(testX)
        algorithm.fit(trainX,trainY)
        try:
            pred = algorithm.predict_proba(testX)
            fpr, tpr, thresholds = roc_curve(testY, pred[:,1], pos_label='Y')
        except:
            pred = algorithm.predict(testX)
            fpr, tpr, thresholds = roc_curve(testY, pred, pos_label='N')
        roc_auc = auc(fpr,tpr)
        roc_auc_s.append(roc_auc)
    # print(roc_auc_s)
    return np.mean(np.array(roc_auc_s))

def algorithmSelect(name):
    if name=='IF':
        #效果奇差
        return IsolationForest()
    elif name=='RF':
        return RandomForestClassifier(120)
    elif name == 'NB':
        return MultinomialNB()
    elif name == 'CART':
        return DecisionTreeClassifier()
    elif name =='SVM':
        return SVC()

if __name__ == '__main__':
    path = '../NASADefectDataset/CleanedData/MDP/D\'\'/'
    for arff_file in os.listdir(path):
        print(arff_file.split('.')[0],end='\t')
        X,Y = processData(path+arff_file)
        for leaner in ['IF','NB','CART','RF']:
            res_auc = bulidClassifier(X, Y, algorithmSelect(leaner), 5)
            if res_auc<0.5:
                res_auc = 1-res_auc
            print(res_auc,end='\t')
        print('')