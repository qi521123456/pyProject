'''
点3，无标记样本分类，无人工干预标记
'''
from time import time

from sklearn import cluster
import numpy as np
from scipy.io import arff
from sklearn.metrics import roc_auc_score,roc_curve
from sklearn.preprocessing import LabelBinarizer
def processData(path):
    X = []
    y = []
    with open(path, 'r') as fr:
        data, meta = arff.loadarff(fr)
        for d in data:
            X.append(tuple(d)[:-1])  # 必须强转
            y.append(d[-1].decode())
    return np.log2(np.mat(X)+1),y
def clustering(X):
    mean = np.mean(X,axis=0)
    bool_diff = X>mean
    diff_num = np.sum(bool_diff==True,axis=1)  # 每个实例中大于中值的个数
    diff_num_mean = np.mean(diff_num,axis=0)
    first_cluster = diff_num>diff_num_mean
    return bool_diff,first_cluster

def select(bool_diff,first_clister):
    instance_num = np.shape(first_clister)[0]
    mvs_diff = (bool_diff==first_clister)
    mvs = np.sum(mvs_diff==False,axis=0)/instance_num
    mvs = mvs.tolist()[0]
    mvs_index = []
    for i in range(10):
        index = mvs.index(np.min(mvs))
        mvs_index.append(index)
        mvs[index] = 1
    bool_diff_mvs = bool_diff[:,mvs_index]
    bdm_b = bool_diff_mvs==first_clister
    ins_index = []
    for i in range(instance_num):
        if first_clister[i]:
            per_uni = np.unique(np.array(bdm_b[i]).tolist())
            if len(per_uni)==1 and per_uni[0]:
                ins_index.append(i)
    return ins_index

def nov_cluster(X,Y):
    for k in range(3,np.shape(X)[1]):
        clf = cluster.KMeans(n_clusters=k)  # 设定k  ！！！！！！！！！！这里就是调用KMeans算法
        s = clf.fit(X)  # 加载数据集合
        centroids = clf.labels_
        print(centroids, type(centroids))# 显示中心点
        print(clf.inertia_)# 显示聚类效果
        from sklearn.cluster import AgglomerativeClustering

        for linkage in ('ward', 'average', 'complete'):
            clustering = AgglomerativeClustering(linkage=linkage, n_clusters=10)
            t0 = time()
            # clustering.fit(X_red)
            # print("%s : %.2fs" % (linkage, time() - t0))
            # plot_clustering(X_red, X, clustering.labels_, "%s linkage" % linkage)

        # pred = cluster.DBSCAN(eps=0.1,min_samples=10).fit_predict(X)
    # bind_width = cluster.estimate_bandwidth(X)
    # clf = cluster.MeanShift(bandwidth=bind_width,bin_seeding=True,cluster_all=True).fit_predict(X)
    # centroids = clf
    # print(centroids, len(centroids))
    # print(Y)
    # print(pred)
    # print(roc_auc_score(Y,pred))
# def nov_pca(X):

if __name__ == '__main__':
    import os
    import matplotlib.pyplot as plt
    PATH = '../NASADefectDataset/CleanedData/MDP/D\'\'/'
    for file in os.listdir(PATH):
        # if not file.startswith('PC4'):
        #     continue
        X, Y = processData(PATH + file)
        # print("name:"+file+"\tfeatures:"+np.shape(X).__str__())
        b,f = clustering(X)
        ins_index = select(b,f)
        pred = np.zeros(np.shape(Y))
        pred[ins_index] = 1
        Y=LabelBinarizer().fit_transform(Y)

        # fpr, tpr, thresholds = roc_curve(Y,pred)
        # print(fpr,tpr)
        # mean_fpr = np.linspace(0, 1, 100)
        # mean_tpr = np.interp(mean_fpr, fpr, tpr)
        # plt.plot(mean_fpr,mean_tpr)
        # plt.show()

        print(file+"\t",roc_auc_score(Y,pred))

        # nov_cluster(X,Y)
