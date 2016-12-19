import re

i=0
flag=False
ip=''
def ipChk(ip_str):
    p = re.compile("^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$")
    if p.match(ip_str):
        return True
    else:
        return False
def titleChk(t_str):
    p=re.compile("\[(.+)\]")
    if p.match(t_str):
        return True
    else:
        return False
filename = 'D:/fofa_result/Result_fingerprint[1].txt'
with open(filename,'r') as fileRead:
    while True:
        #try:
        line=next(fileRead)
        #except StopIteration:
            #break
        if not line:
            break
        if titleChk(line):

            flag=True
        if line.strip() == 'Auto_ip:':
            i += 1
            ip=next(fileRead).strip()
           # print(next(fileRead)+'-----' + str(i))
        if line == 'Auto_port:':
            port=next(fileRead).strip()
        else:
            port='--'
        print('======'+ip,port,'==='+str(i))
fileRead.close()