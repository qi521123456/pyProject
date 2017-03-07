import numpy as np


t = np.tile([2,1],(4,1))
d = {'A':1}
print(d.get('A',2))

L = [('b',2),('a',1),('c',3),('d',4)]
print(sorted(L, key=lambda x:x[1]))