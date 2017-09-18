import os
def splitips(file,n):
    l = []
    with open(file,'r') as fr:
        lines = fr.readlines()
        for i in range(n):
            l.append([])
        for i,line in enumerate(lines):
            for j in range(n):
                if i%n==j:
                    l[j].append(line)
    return l

def toNfile(path,file,n):
    if not os.path.exists(path):
        os.makedirs(path)
    l = splitips(file,n)
    for i,il in enumerate(l):
        write_file = path+str(i)+".txt"
        with open(write_file,'w',encoding="utf8") as fw:
            fw.writelines(il)
def spp(hosts,file,path):
    nh = len(hosts)
    l = []
    n = nh
    with open(file, 'r') as fr:
        lines = fr.readlines()
        nl = len(lines)
        if nh>nl:
            n = nl
        for i in range(n):
            l.append([])
        for i, line in enumerate(lines):
            for j in range(n):
                if i % n == j:
                    l[j].append(line)
    hs = hosts[:n]
    for i,il in enumerate(l):
        write_file = path+hs[i]+".txt"
        with open(write_file,'w',encoding="utf8") as fw:
            fw.writelines(il)
    return n
if __name__ == '__main__':
    #toNfile("E:/q1/","E:/1.txt",57)
    #toNfile("E:/q11/110000/", "E:/110000.txt", 18)
    hs = ['docker1@192.168.202.1','docker2']
    n = spp(hs,"E:/1.txt","e:/1/")
    print(n)
