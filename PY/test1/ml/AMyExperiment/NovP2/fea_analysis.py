import os
from scipy.io import arff
import numpy as np

WEIGHT = 150

def processData(path):
    X = []
    y = []
    with open(path, 'r') as fr:
        data, meta = arff.loadarff(fr)
        for d in data:
            X.append(tuple(d)[:-1])  # 必须强转
            y.append(d[-1].decode())
    return meta.names(),np.array(X), np.array(y)


def calc_ent(x):
    """
        calculate shanno ent of x
    """
    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]

        logp = np.log2(p)
        ent -= p * logp
    return ent


def calc_condition_ent(x, y):
    """
        calculate ent H(y|x)
    """
    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    for x_value in x_value_list:
        sub_y = y[x == x_value]
        temp_ent = calc_ent(sub_y)
        ent += (float(sub_y.shape[0]) / y.shape[0]) * temp_ent

    return ent


def calc_ent_gain(x, y):
    """
        calculate ent gain
    """
    base_ent = calc_ent(y)
    condition_ent = calc_condition_ent(x, y)
    ent_grap = base_ent - condition_ent
    return ent_grap


def _calc_gain_ratio(x, y):
    gain = calc_ent_gain(x, y)
    temp_ent = calc_ent(x)
    return gain/temp_ent

def calc_gini(x):
    x_value_list = set([x[i] for i in range(x.shape[0])])
    gini = 1.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]
        ynum = x[x == 'Y'].shape[0]
        # if x_value=='Y':
        #     p = float(ynum*WEIGHT) / (x.shape[0]-ynum+ynum*WEIGHT)
        # else:
        #     p = float(x.shape[0] - ynum) / (x.shape[0] - ynum + ynum * WEIGHT)
        gini -= p * p
    return gini
def calc_gini_index(x,y):
    x_value_list = set([x[i] for i in range(x.shape[0])])
    gini_index = 0.0
    for x_value in x_value_list:
        sub_y = y[x == x_value]
        tmp_gini = calc_gini(sub_y)
        gini_index += (float(sub_y.shape[0]) / y.shape[0]) * tmp_gini
    return gini_index

def run(x,y):
    gain_ratio = []
    gains = []
    gini_indexs = []
    fea_list = [x[:, i] for i in range(x.shape[1])]
    for i, fea in enumerate(fea_list):
        fea = fea.T
        gain = calc_ent_gain(fea, y)
        temp_ent = calc_ent(fea)
        gini_index = calc_gini_index(fea,y)
        gain_ratio.append(gain / temp_ent)
        gains.append(gain)
        gini_indexs.append(gini_index)
        # print('%s\t%s\t%s\t%s' % (i, gain, gain / temp_ent,gini_index))
    return gains.index(max(gains)), gain_ratio.index(max(gain_ratio)),gini_indexs.index(min(gini_indexs))

def _choseFirstFeatureGini(X,Y):
    X = np.array(X, dtype='float64')
    Y = np.array(Y)
    numFeatures = len(X[0])
    numSimples = len(X)
    bestGini = 999999.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = X[:,i]
        uniqueVals = np.unique(featList)
        gini = 0.0
        for value in uniqueVals:
            indics = np.where(featList==value)
            # print(indics)
            subY = Y[indics]
            prob = len(subY)/float(numSimples)
            subProb = np.where(subY=='Y')[0].shape[0]/float(len(subY))
            # if subProb==0:
            #     print("--------")
            # else:
            #     print('+++++++')
            # gini += prob * (1.0 - pow(subProb, 2) - pow(1 - subProb, 2))
            # gini += prob*2*subProb*(1-subProb)
            gini += prob*calc_gini(subY)
        gini*=len(uniqueVals)
        if (gini < bestGini):
            bestGini = gini
            bestFeature = i
    return bestFeature
if __name__ == '__main__':
    path = '../NASADefectDataset/CleanedData/MDP/D\'\'/'
    for arff_file in os.listdir(path):
        print(arff_file.split('.')[0], end='\t')
        names, X, Y = processData(path + arff_file)
        WEIGHT = Y[Y=='Y'].shape[0]/float(Y[Y=='N'].shape[0])
        a,b,c = run(X, Y)
        c2 = _choseFirstFeatureGini(X,Y)
        print('%s:%s\t%s:%s\t%s:%s\t%s:%s'%(names[a],a,names[b],b,names[c],c,names[c2],c2))

    # print(np.log2(0))