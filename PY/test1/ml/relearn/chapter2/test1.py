import numpy as np

def t1():
    t = np.tile([2,1],(4,1))
    d = {'A':1}
    print(d.get('A',2))

    L = [('b',2),('a',1),('c',3),('d',4)]
    print(sorted(L, key=lambda x:x[1]))

def t2():
    # print(np.zeros((2,3)))
    # print(np.array([1,3]),np.mat([1,3]))
    m = np.zeros((3,5))
    print(m[1,:])


t2()