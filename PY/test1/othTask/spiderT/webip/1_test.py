import requests
import json,datetime

def getdata(ips,port):
    l = []
    for ip in ips:
        if port==80:
            url = "http://"+ip
        elif port==443:
            url = "https://"+ip
        else:
            url = "http://"+ip+":"+str(port)
        data = {}
        data['port'] = port
        data['time'] = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        data['ip'] = ip
        try:
            q = requests.get(url, timeout=3)
            data['status_code'] = q.status_code
            data['header'] = dict(q.headers)
            data['content'] = str(q.content)
        except requests.exceptions.ConnectTimeout:
            data['status_code'] = ""
            data['header'] = ""
            data['content'] = ""
        l.append(data)
    return l
def splitips(file):
    ips_1 = []
    ips_2 = []
    ips_3 = []
    ips_4 = []
    ips_5 = []
    with open(file,'r') as fr:
        lines = fr.readlines()
        for i,line in enumerate(lines):
            if i%5==0:
                ips_1.append(line)
            elif i%5==1:
                ips_2.append(line)
            elif i%5==2:
                ips_3.append(line)
            elif i%5==3:
                ips_4.append(line)
            else:
                ips_5.append(line)

def data2json(data,file):
    with open(file,'w') as fw:
        for i in data:
            fw.write(json.dumps(i)+'\n')


if __name__ == '__main__':
    l = getdata(["175.148.64.18","166.166.166.166"],80)
    data2json(l,'E:/test.json')