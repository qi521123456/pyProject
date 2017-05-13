# coding:utf-8
import numpy as np
import os
import kNN


def img2vector(filename):
    vectlist = []
    with open(filename,'r') as fr:
        lines = fr.readlines()
    for line in lines:
        for i in line.strip():
            vectlist.append(int(i))
    vect = np.array(vectlist)
    # print(vect[0,0:31])
    return vect

def main(trainingpath,testpath):
    trainfiles = os.listdir(trainingpath)
    m = len(trainfiles)
    trainMat = np.zeros((m,1024))
    labels = []
    for i in range(m):
        filename = trainfiles[i]
        labNum = int(filename.split('_')[0])
        labels.append(labNum)
        trainMat[i,] = img2vector(trainingpath+filename)
    testfiles = os.listdir(testpath)
    n = len(testfiles)
    for i in range(n):
        filename = testfiles[i]
        label = int(filename.split('_')[0])
        testvect = img2vector(testpath+filename)
        res = kNN.classify0(testvect,trainMat,labels,3)
        print("knn得：%d,实际：%d"%(res,label))



main("G:/Study/ml/MLiA_SourceCode/machinelearninginaction/Ch02/trainingDigits/",
     "G:/Study/ml/MLiA_SourceCode/machinelearninginaction/Ch02/testDigits/")

