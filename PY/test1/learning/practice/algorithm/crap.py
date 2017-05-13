
def craps(n, s):
    if s < n or s > 6*n:
        print('wrong s number')
        return -1






def reOrderArray(array):
    l = []
    r = []
    for i in range(len(array)):
        if array[i] % 2 == 1:
            l.append(array[i])
        else:
            r.append(array[i])
    l.extend(r)
    return l

print(reOrderArray([1,2,3,4,5,6,7]))