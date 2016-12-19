#coding utf-8
alltext=open('D:\PY\hello.py').read()
#print(alltext)
alldata=open('C:/Users/LMQ/Desktop/S7Comm.txt','rb').read()
#print(alldata)
fileObj=open('C:/Users/LMQ/Desktop/S7Comm.txt')
try:
    allTxt=fileObj.read()
finally:
    fileObj.close()
print(allTxt)