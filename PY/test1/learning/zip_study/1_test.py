import zipfile
def tozip():
    f = zipfile.ZipFile('D:/test.zip', 'w', zipfile.ZIP_DEFLATED)
    f.write('D:/yyx.log')
    f.write('D:/spam.log')
    f.write('D:/styles.xlsx')
    f.close()
def upzip():
    f = zipfile.ZipFile('D:/test.zip')
    f.extractall('D:/')
    f.close()

# upzip()

# with open('D:/test.zip','rb') as zfile:
#     result = zfile.read()

with zipfile.ZipFile('D:/new.zip','w',compression=zipfile.ZIP_DEFLATED) as new:
   new.write("D:/hello.txt","oo.txt")

