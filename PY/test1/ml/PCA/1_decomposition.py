import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#%matplotlib inline
from sklearn.datasets.samples_generator import make_blobs

from sklearn.decomposition import PCA

# X为样本特征，Y为样本簇类别， 共1000个样本，每个样本3个特征，共4个簇
X, y = make_blobs(n_samples=10000, n_features=3, centers=[[3,3, 3], [0,0,0], [1,1,1], [2,2,2]], cluster_std=[0.2, 0.1, 0.2, 0.2],random_state=9)
# print(X)
fig = plt.figure()
ax = Axes3D(fig, rect=[0, 0, 1, 1], elev=30, azim=20)
# ax.set_zlim(-0.01,0.1)

pca = PCA(n_components=0.98,svd_solver='full') # 只有svd_solver=‘full’ 时才可设置 n_components=‘mle’ 即自动降维
pca.fit(X)
a = pca.transform(X)
print(a)
plt.scatter(X[:, 0], X[:, 1], X[:, 2],marker='o')
# print(pca.n_components_)
# print(pca.explained_variance_ratio_)
# print(pca.explained_variance_)
plt.show()