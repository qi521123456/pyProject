import os,sys
def parse(file):
    with open(file,'r') as fr:
        lines = fr.readlines()
        for line in lines:
            name = line.split("\t")[0]
            f = line.split("\t")[1]
            if "||" in f:
                print("# "+name,f)
                continue
            fl = f.strip().split("&&")
            esq = '''{"name":"''' + name + '''","query":'{"bool":{"must":[{"time":"'+time+'"},'''
            for i in fl:
                j = i.strip().split("=")
                j[1] = j[1].strip('"')
                esq += '{"'+j[0]+'":"'+j[1]+'"},'

            esq = esq[:-1]
            esq += "]}}'},"
            print(esq)


if __name__ == '__main__':
    file = "/home/mannix/Desktop/test.txt"
    parse(file)
    # print(",wif,".strip(','))