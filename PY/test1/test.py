# teams = ["Packers", "49ers", "Ravens", "Patriots"]
# print({key: value for value, key in enumerate(teams)})
#
# x = [1,2,3,4,5,6,7]
# print(x[2::])

# print('fizz'[2::])

# for x in range(101):
#     print("fizz"[x%3*4::]+"buzz"[x%5*4::]or x)
#
# import time
# ids = dict()
# li = list()
# i = time.time()
# ids[i] = 1
# ids.pop(i)
# print(ids.get(i),ids,li)

# ids = None
# def creat():
#     ids = (1,'ttt')
#     print(ids)
# creat()

# import os
# import time
# print(os.path.exists('127.0.0.1'))
# with open('D:/res.txt') as f:
#     for line in f.readlines():
#         print(line.strip())
#
# print(time.ctime())

# def foo(arg1,*tupleArg,**dictArg):
#     print("arg1=",arg1 ) #formal_args
#     print ("tupleArg=",tupleArg ) #()
#     print ("dictArg=",dictArg )  #[]
# foo(9,9,9,9,9,9,9,{'s':5,6:4},l=3)

# import re,os
# print(re.search('w3w','2www/33rew'))
str1 = 'wft4wrt/rgrs'
print(str1.rfind('/'),str1[:str1.rfind('/')],str1[7:])
# print('wertrd/24'.split('/'))
#
# print(os.path.exists('d:/tmp/script'))

#print(['Google', 'Runoob', 'Taobao', 'Baidu'][::-1])
# for i in [2, 3, 4].reverse():
#     print(i)
import sys,os
print(r'D:\WorkFile\PY\test1' in sys.path,sys.path)
print(sys.path[0][:sys.path[0].rfind('\\')],os.getcwd())