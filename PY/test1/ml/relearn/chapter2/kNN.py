from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt

def createDataSet():
    group = array([[1.0,1.1],[1.1,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distance = sqDistances**0.5
    sortedDistIndicies = distance.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    with open(filename,'r') as fr:
        lines = fr.readlines()
        fr.close()
    num_lines = len(lines)
    matrix = zeros((num_lines,3))
    classLabelVector = []
    index = 0
    for line in lines:
        line = line.strip()
        list_line = line.split('\t')
        matrix[index,:] = list_line[0:3]
        classLabelVector.append(int(list_line[-1]))
        index += 1
    return matrix,classLabelVector

def pltshow(datingDataMat,labels):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:,0], datingDataMat[:,1],
               15.0*array(labels), 15.0*array(labels))
    plt.show()
if __name__ == "__main__":
    r = file2matrix(r"G:\Study\机器学习实战\MLiA_SourceCode\machinelearninginaction\Ch02\datingTestSet2.txt")
    pltshow(r[0],r[1])
    #print(r[0][:,1])