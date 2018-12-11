import numpy as np
from scipy.io import arff
from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score
from sklearn import cluster
def load_data(path):
    X = []
    y = []
    with open(path, 'r') as fr:
        data, meta = arff.loadarff(fr)
        for d in data:
            X.append(tuple(d)[:-1])
            y.append(d[-1].decode())
    return np.log2(np.mat(X) + 1), y
def _pca(X,n_com=10):
    pca = PCA(n_components=n_com)
    X = pca.fit_transform(X)
    return X
def _init_cluster(X):
    gap_pos = []
    for arr in X.T:
        tmp = np.sort(arr)
        max_gap = 0
        pre = 0
        for i,v in enumerate(tmp):
            if i==0:
                pre = v
                continue
            if v-pre>max_gap:
                max_gap = v
            pre = v
        gap_pos.append(max_gap)
    return X>=gap_pos
def _label_mvs(X):
    label = np.sum(X,axis=1)
    distinct = np.array(list(set(label)))
    threshold = np.sum(distinct)/len(distinct)
    label = label>=threshold
    label = np.reshape(label,(len(label),1))
    mvs = np.sum(X==label,axis=0)/float(len(label))
    mvs_threshold = np.sum(mvs)/len(mvs)
    fea_indics = np.where(mvs>mvs_threshold)[0].tolist()

    X = X[:,fea_indics]
    ins_mvs = np.sum(X == label, axis=1)
    ins_mvs_threshold = list(set(ins_mvs))[len(set(ins_mvs))//2]
    ins_indics = np.where(ins_mvs>=ins_mvs_threshold)[0].tolist()

    return label,ins_indics,fea_indics

if __name__ == '__main__':
    import os
    PATH = '../NASADefectDataset/CleanedData/MDP/D\'\'/'
    for file in os.listdir(PATH):
        X, Y = load_data(PATH+file)
        Y = np.reshape(Y, (len(Y), 1))

        X_t = _pca(X,np.shape(X)[1]//2)
        X_t = _init_cluster(X_t)
        lable,ins_indics,fea_indics = _label_mvs(X_t)
        y_true = []
        for i in Y:
            if i=='Y':
                y_true.append(1)
            else:
                y_true.append(0)
        # print(np.shape(y_true),np.sum(y_true=='Y'))
        # print(np.shape(X[:,fea_indics]),np.sum(lable))
        clf = cluster.KMeans(n_clusters=2,n_init=20).fit(X[:,fea_indics])
        # ac = cluster.AgglomerativeClustering(n_clusters=2,linkage='complete').fit(X[:,fea_indics])
        # clf = cluster.DBSCAN(min_samples=2).fit(X[:,fea_indics])
        print(roc_auc_score(y_true,clf.labels_))

