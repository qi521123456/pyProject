from scipy.io import arff
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.ensemble import IsolationForest,RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
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
def algorithmSelect(name):
    if name=='IF':
        #效果奇差
        return IsolationForest()
    elif name=='RF':
        return RandomForestClassifier(140)
    elif name == 'NB':
        return MultinomialNB()
def attrsSelect(X,y,algorithm,m,n):
    pass

def bulidClassifier(X,y,algorithm):
    # iforest = IsolationForest()
    X = np.array(X,dtype='float64')
    scaler = Normalizer()
    trainX,testX,trainY,testY = train_test_split(X,y,test_size=0.2)
    trainX = scaler.fit_transform(trainX)
    testX = scaler.fit_transform(testX)

    algorithm.fit(trainX,trainY)

    pred = algorithm.predict_proba(testX)
    # print(pred,testY)
    fpr, tpr, thresholds = roc_curve(testY, pred[:,1], pos_label='Y')
    roc_auc = auc(fpr,tpr)
    print(roc_auc)

if __name__ == '__main__':
    PATH = '../NASADefectDataset/CleanedData/MDP/D\'\'/CM1.arff'
    X,Y = processData(PATH)
    for i in range(9,150):
        print(i,end='\t')
        bulidClassifier(X,Y,RandomForestClassifier(i))