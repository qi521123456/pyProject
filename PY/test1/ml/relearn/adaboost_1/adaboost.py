import numpy as np
def loadSimpData():
    datMat = np.matrix([[1.,2.1],[2.,1.1],[1.3,1.],[1.,1.],[2.,1.]])

if __name__ == '__main__':
    #print(np.shape(np.mat([[1.,2.1],[2.,1.1],[1.3,1.],[1.,1.],[2.,1.]])))
    l = np.mat([[1,2],[3,4],[5,6]])
    a = np.mat([[1],[1],[1]])
    #a[<=2] = -1
    print(l[:2, 0])
    a[l[:, 1] <= 2] = -1
    print(np.ones(55))