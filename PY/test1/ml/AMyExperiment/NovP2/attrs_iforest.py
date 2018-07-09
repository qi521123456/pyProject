from scipy.io import arff
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.ensemble import IsolationForest
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
def attrsSelect(X,y,algorithm,m,n):
    np.log2()

def bulidClassifier(X,y,algorithm):
    iforest = IsolationForest()
    scaler = Normalizer()
    trainX,testX,trainY,testY = train_test_split(X,y,test_size=0.2)
    trainX = scaler.fit_transform()
    iforest.fit(trainX,trainY)
    pred = iforest.predict(testX)
    print(pred,testY)
    fpr, tpr, thresholds = roc_curve(testY, pred, pos_label='Y')
    print(auc(fpr,tpr))

if __name__ == '__main__':
    PATH = '../NASADefectDataset/CleanedData/MDP/D\'\'/CM1.arff'
    X,Y = processData(PATH)
    bulidClassifier(X,Y,None)