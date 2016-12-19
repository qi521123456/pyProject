from itertools import combinations
def twoSum_1(nums, target):
    for twonum in combinations(nums,2):
        if twonum[0]+twonum[1] == target:
            print(twonum)
def twoSum_2(nums,target):
    for i in range(len(nums)):
        for j in range(i+1,len(nums)):
            if nums[i]+nums[j] == target:
                print('[%d,%d]'%(i,j))
                return [i,j]

def  twoSum_3(nums,target):
    for i,x in enumerate(nums):
        for j,y in enumerate(nums):
            if x+y == target and i!= j:
                return [i,j]

# nums = [2,2, 7, 11, 15]
# print(twoSum_3([3,2,4],6))
#--------------------------------------

def ts2_1(nums,targets):
    pass
