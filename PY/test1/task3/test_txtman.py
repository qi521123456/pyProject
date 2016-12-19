import re

i=0
iflag=False
pflag=False
tflag=False
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
    lines = fileRead.readlines()  # 读取全部内容
    for line in lines:
        if not line:
            break
        if titleChk(line.strip()):
            i += 1
            tflag = True
        if iflag:
            print(line + '------------' + str(i))
            iflag = False
        if pflag:
            print(line + '+++++++++++++' + str(i))
            pflag = False

        if line.strip() == 'Auto_ip:':
           # ip=next(fileRead)

            iflag=True

            #print(ip + '------' + str(i))
        if line.strip() == 'Auto_port:':
            #port = next(fileRead)
            pflag=True
            #print('++++++++++++++' + port + '++++++++++++++' + str(i))





fileRead.close()


