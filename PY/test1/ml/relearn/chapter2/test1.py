import numpy as np


t = np.tile([2,1],(4,1))
d = {'A':1}
print(d.get('A',2))