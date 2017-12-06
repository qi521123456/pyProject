
def getData(path):
    data = {}
    with open(path,'r') as fr:
        for line in fr:
            l = line.split(',')
            data[l[-1]] = 0