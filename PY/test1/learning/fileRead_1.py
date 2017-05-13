#coding utf-8
# alltext=open('D:\PY\hello.py').read()
# #print(alltext)
# alldata=open('C:/Users/LMQ/Desktop/S7Comm.txt','rb').read()
# #print(alldata)
# fileObj=open('C:/Users/LMQ/Desktop/S7Comm.txt')
# try:
#     allTxt=fileObj.read()
# finally:
#     fileObj.close()
# print(allTxt)

def test1(path):
    with open(path) as ifile:
        for line in ifile:  # 默认为readlines
            print(line,'----')

test1("F:/1.txt")