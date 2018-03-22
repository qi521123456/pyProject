from scipy.io import arff
import os
PATH = "/home/mannix/Desktop/NASADefectDataset/CleanedData/MDP/D'/"

def _getData(file):
    X = []
    y = []
    with open(file,'r') as fr:
        data,meta = arff.loadarff(fr)
        for d in data:
            X.append(tuple(d)[:-1])  # 必须强转
            y.append(d[-1].decode())
    return X,y
def AllData():
    data = []
    for file in os.listdir(PATH):

        path_file = os.path.join(PATH,file)
        X,y = _getData(path_file)
        d = {}
        d['name'] = file[:-5]
        d['X'] = X
        d['y'] = y
        data.append(d)
    return data

if __name__ == '__main__':

    print("----",end='')
    print("++++++++")