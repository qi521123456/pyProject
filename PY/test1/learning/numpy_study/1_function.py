from numpy import *

l = array([[1],[1],[2]])
print(l.shape,l.T)
d = tile(array([1.2,3]), (4, 1))
print(sum(d-1,axis=1)**0.5)

li = [4,3,2,5,6,7]
a = argsort(li)
print(li,a)

print(exp(0),random.random((3, 1)))