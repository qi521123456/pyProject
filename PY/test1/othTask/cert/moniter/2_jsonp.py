import sys
path = "E:/ips.txt"
def getinfo(s):
    with open(path,'r',encoding="utf8") as fr:
        for line in fr:
            d = eval(line)
            print(d.get(s))




if __name__ == '__main__':
    getinfo(sys.argv[1])