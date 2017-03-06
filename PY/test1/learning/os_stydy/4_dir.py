import os
path = "D:/test_e/"
print(os.path.isdir(path),os.path.isfile(path),os.path.exists(path))
print(os.listdir(path))
print(os.path.splitext(path+'ttt.txt'))
for i in os.listdir(path):
    print(i)