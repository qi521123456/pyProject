import numpy as np

l = [2,3,4,5,7]
# print(l)
# del l[2]
# print(int(np.random.uniform(0, 4)))

l2 = np.mat(l)
np.delete(l2,0,0)
print(l2)