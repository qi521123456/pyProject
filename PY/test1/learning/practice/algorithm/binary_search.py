def binSearch(l,x,low=0,high=-1):
    # if high == -1:
    #     high = len(l) - 1
    if low > high:
        return -1
    middle = (low+high)//2
    if l[middle] == x:
        return str(middle)
    elif l[middle] < x:
        return (binSearch(l,x,middle+1,high))
    else:
        return (binSearch(l,x,low,middle-1))

def binS_lo(l,x,low,high):
    while low<=high:
        middle = (low+high)//2
        if l[middle] == x:
            return middle
        elif l[middle]<x:
            low = middle+1
        else:
            high = middle - 1
    return -1


class Solution:
    # array 二维列表
    def binSearch(self, l, x, low=0, high=-1):
        if low > high:
            return -1
        middle = (low + high) // 2
        if l[middle] == x:
            return str(middle)
        elif l[middle] < x:
            return (binSearch(l, x, middle + 1, high))
        else:
            return (binSearch(l, x, low, middle - 1))

    def Find(self, target, array):
        # write code here
        # for l in array:
        #     if self.binSearch(l, target, 0, len(l) - 1) != -1:
        #         return True
        # return False
        for l in array:
            low = 0
            high = len(l)-1
            while low <= high:
                middle = (low + high) // 2
                if l[middle] == target:
                    return True
                elif l[middle] < target:
                    low = middle + 1
                else:
                    high = middle - 1
        return False


sol = Solution()
l = [[1,2,8,9],[2,4,9,12],[4,7,10,13],[6,8,11,15]]
print(sol.Find(7,l),binS_lo(l[0],8,0,3),2 in l)

# --------------------------------------
# matrix查找===========================出错
def msearch(l,x):
    i = 0
    for i in range(len(l)):
        if l[i][i] == x:
            return True
        elif l[i][i] < x:
            continue
        else:
            break
    if i == range(len(l)):
        return False
    rh = []
    ll = []
    j = 0
    for sub in l:
        if j<i:
            rh.append(sub[i:])
        else:
            ll.append(sub[:i+1])
    return msearch(rh,x),msearch(ll,x)


#print(msearch(l,7))

# ------左下角开始小
def mresc(l,x):
    i = len(l)-1
    j = 0
    while i>-1 and j<len(l[0]):
        if x==l[i][j]:
            return True
        elif x<l[i][j]:
            i -= 1
        else:
            j += 1
    return False
print(mresc(l,1111))




