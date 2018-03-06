import numpy as np
# abalone 实验
PATH = "D:/abalone.txt"
def getData(path=PATH):
    X = []
    y = []
    with open(path,'r') as fr:
        lines = fr.readlines()
        for line in lines:
            perdata = line.strip().split(",")
            X.append(perdata[:-1])
            if int(perdata[-1])>=17:
                y.append(0)
            else:y.append(1)
    return X,y

def train_test(X,y,test_size=0.4):
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    return np.array(X_train),np.array(X_test),np.array(y_train),np.array(y_test)

def pca_x(X,n=2):
    from sklearn.decomposition import PCA
    X = np.array(X,dtype='float64') # dtype 转化数字类型，pca中做减法时需要
    pca = PCA(n_components=n)
    pca.fit(X)
    x_reduce = pca.transform(X)
    return x_reduce
if __name__ == '__main__':
    X,y = getData(PATH)
    X_train, X_test, y_train, y_test = train_test(X,y,0.5)
    x2d = pca_x(X_train,2)

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # fig = plt.figure()
    # ax = Axes3D(fig, rect=[0, 0, 1, 1], elev=30, azim=20)
    plt.scatter(x2d[:,0],x2d[:,1], marker='o', c=y_train)
    plt.show()
    # for i,x in enumerate(x2d):
    #
    #     print(str(i)+"--"+str(x)+"++"+str(y_train[i]))