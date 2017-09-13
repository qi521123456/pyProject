import os,time

f = "E:/111.txt"
mtime = time.ctime(os.path.getmtime(f))
ctime = time.ctime(os.path.getctime(f))
print(time.strftime("%H:%M:%S",time.localtime(os.path.getmtime(f))))
print(time.strftime("%H:%M:%S",time.localtime(time.time())))
x = time.time()-os.path.getmtime(f)
print(x,time.strftime("%H:%M:%S",time.localtime(x)))
if x>60:
    print("hello")