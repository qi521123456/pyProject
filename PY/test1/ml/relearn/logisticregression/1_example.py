from numpy import *
import matplotlib.pyplot as plt


def sigmoid(X):
    return 1.0 / (1 + exp(-X))


class logRegressClassifier(object):
    def __init__(self):
        self.dataMat = list()
        self.labelMat = list()
        self.weights = list()

    def loadDataSet(self, filename):
        fr = open(filename)
        for line in fr.readlines():
            lineArr = line.strip().split()
            dataLine = [1.0]
            for i in lineArr:
                dataLine.append(float(i))
            label = dataLine.pop()  # pop the last column referring to  label
            print(label)
            self.dataMat.append(dataLine[:2])
            self.labelMat.append(int(label))
        self.dataMat = mat(self.dataMat)
        self.labelMat = mat(self.labelMat).transpose()

    def train(self):
        self.weights = self.stocGradAscent1()

    def batchGradAscent(self):
        m, n = shape(self.dataMat)
        alpha = 0.001
        maxCycles = 500
        weights = ones((n, 1))
        for k in range(maxCycles):  # heavy on matrix operations
            h = sigmoid(self.dataMat * weights)  # matrix mult
            error = (self.labelMat - h)  # vector subtraction
            weights += alpha * self.dataMat.transpose() * error  # matrix mult
        return weights

    def stocGradAscent1(self):
        m, n = shape(self.dataMat)
        alpha = 0.01
        weights = ones((n, 1))  # initialize to all ones
        for i in range(m):
            h = sigmoid(sum(self.dataMat[i] * weights))
            error = self.labelMat[i] - h
            weights += (alpha * error * self.dataMat[i]).transpose()
        return weights

    def stocGradAscent2(self):
        numIter = 2
        m, n = shape(self.dataMat)
        weights = ones((n, 1))  # initialize to all ones
        for j in range(numIter):
            dataIndex = list(range(m))
            for i in range(m):
                alpha = 4 / (1.0 + j + i) + 0.0001  # apha decreases with iteration, does not
                randIndex = int(random.uniform(0, len(dataIndex)))  # go to 0 because of the constant
                h = sigmoid(sum(self.dataMat[randIndex] * weights))
                error = self.labelMat[randIndex] - h
                weights += (alpha * error * self.dataMat[randIndex]).transpose()
                del (dataIndex[randIndex])
        return weights

    def classify(self, X):
        prob = sigmoid(sum(X * self.weights))
        if prob > 0.5:
            return 1.0
        else:
            return 0.0

    def test(self,datafile):
        self.loadDataSet(datafile)
        weights0 = self.batchGradAscent()
        weights1 = self.stocGradAscent1()
        weights2 = self.stocGradAscent2()
        print('batchGradAscent:', weights0)
        print('stocGradAscent0:', weights1)
        print('stocGradAscent1:', weights2)
        self.weights = weights2
        print(self.classify([0.423363,11.054677]))

if __name__ == '__main__':
    lr = logRegressClassifier()
    lr.test(r'C:\Users\LMQ\Desktop\论文\机器学习实战及配套代码\机器学习实战及配套代码\MLiA_SourceCode\machinelearninginaction\Ch05\testSet.txt')