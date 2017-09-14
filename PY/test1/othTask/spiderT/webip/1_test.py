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
            q = requests.get(url, timeout=1)
            print(q)
            data['status_code'] = q.status_code
            data['header'] = dict(q.headers)
            data['content'] = str(q.content)
        except:  # connectionTimeout,readTimeout,
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
    with open(file,'a+',encoding='utf8') as fw:
        for i in data:
            try:
                fw.write(json.dumps(i)+'\n')
            except:
                pass


def main(ipfile,port,writefile,n=100):
    with open(ipfile,'r') as fr:
        lines = fr.readlines()
        write_lines = []
        for i,ip in enumerate(lines):
            write_lines.append(ip.strip())
            if i%n==0 and i!=0:
                data2json(getdata(write_lines,port),writefile)
                write_lines = []
        if len(write_lines)!=0:
            data2json(getdata(write_lines, port), writefile)


if __name__ == '__main__':
    main("E:/80port.txt",80,"E:/test.json",100)