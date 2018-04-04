import datetime,time
def get_target(file_name, factor, seq):
    with open(file_name, encoding='UTF-8') as f:
        lines = f.readlines()
    targets = []
    try:
        if (factor - seq) is 1:
            targets = lines[seq * (len(lines) // factor):len(lines)]
        else:
            targets = lines[seq * len(lines) // factor: (seq + 1) * len(lines) // factor]
    except RuntimeError:
        pass
    return targets
def new_get_target(file_name, factor, seq):
    with open(file_name, encoding='UTF-8') as f:
        lines = f.readlines()
    targets = []
    try:
        if factor is 1 and seq is 0:
            return lines
        for i in range(0,len(lines)):
            if i%factor is seq:
                targets.append(lines[i])
    except RuntimeError:
        pass
    return targets

def writefile(filename):
    with open(filename,'w',encoding='UTF-8') as fw:
        for i in range(1,100001):
            fw.write(str(i)+'\n')


if __name__ == '__main__':
    filename = 'D:/iptest.txt'
    import os
    import numpy as np
    a = np.array([1,2,3])
    b = np.array([1,2,3])
    print()
    # writefile(filename)
    # starttime = datetime.datetime.now()
    # txt = get_target(filename,1,0)
    # endtime = datetime.datetime.now()
    # print(endtime-starttime)
    # print(txt)
    #n你现在
