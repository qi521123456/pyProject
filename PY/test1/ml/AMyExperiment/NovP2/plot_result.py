import matplotlib.pyplot as plt

def getResult(path):
    axliX = []
    axlY1 = []
    axlY2 = []
    axlY3 = []
    with open(path,'r') as fr:
        for line in fr:
            data = line.split('\t')
            axliX.append(data[0])
            axlY1.append(data[1])
            axlY2.append(data[2])
            axlY3.append(data[3])
    return axliX,axlY1,axlY2,axlY3

def plotLine(x,y1,y2,y3):
    plt.figure()
    plt.plot(x,y1,label='RF')
    plt.plot(x, y2, label='NB')
    plt.plot(x, y3, label='IF')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    x, y1, y2, y3 = getResult('./Result/7-11.txt')
    plotLine(x, y1, y2, y3)

