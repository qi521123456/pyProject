l = [2,3,4,5,6]
print(l[-2:])

l2 = range(1,4)
print(l2[1])


from functools import reduce
print(reduce(lambda x,y:x*y,range(1,4)))