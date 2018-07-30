import argparse,sys

import requests
import json,datetime
import os,time
from bs4 import BeautifulSoup
import demjson

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
            data['status_code'] = q.status_code
            q_header = {}
            qh = dict(q.headers)
            for k in qh:
                if k is not None and qh[k] is not None:
                    if k=="Last-Modified" or k=="Date":
                        st = qh[k]
                        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
                        try:
                            d = datetime.datetime.strptime(st, GMT_FORMAT)
                            if not isinstance(d,datetime.datetime):
                                continue
                        except:
                            continue
                    try:
                        if len(k)<3 or type(int(k))==int:
                            continue
                    except:
                        pass
                    q_header[k.strip('').strip('.').replace('.','-').lower()] = qh[k].strip('').strip('.')
                    # q_header[k.strip('').strip('.').replace('.','-')] = qh[k].strip('').strip('.')
            data['server'] =q_header
            soup = BeautifulSoup(q.content,from_encoding='utf8')
            head = {}
            body = ""
            try:
                for bodystr in soup.body.stripped_strings:
                    body += "\t" + bodystr
                data['body'] = body.strip()

                head['title'] = soup.title.string
                for child in soup.head.children:
                    if child.name=="meta":
                        attr = child.attrs
                        if attr.get('name') is not None:
                            key = attr['name'].strip('.').replace('.','-')
                            value = attr['content']
                            if key.lower().find("date")!=-1 or key.find("DC")!=-1:
                                continue
                            head[key]=value
                data['head'] = head
            except:
                pass
        except:  # connectionTimeout,readTimeout,
            data['head'] = ""
            data['body'] = ""
        l.append(data)
    return l

def data2json(data,file):
    with open(file,'a+',encoding='utf8') as fw:
        for i in data:
            try:
                fw.write(json.dumps(i)+'\n')
            except:
                pass


def main(ipfile,port,writepath,n=100,perfileN=10000):
    if not os.path.exists(writepath):
        os.makedirs(writepath)
    with open(ipfile,'r') as fr:
        lines = fr.readlines()
        write_lines = []
        x = 1
        writefile = writepath+"hello.json"
        for i,ip in enumerate(lines):
            write_lines.append(ip.strip())
            if i%perfileN==0:
                writefile = writepath + str(x) + ".json"
                x += 1
            if i%n==0 and i!=0:
                data2json(getdata(write_lines,port),writefile)
                write_lines = []
        if len(write_lines)!=0:
            data2json(getdata(write_lines, port), writefile)


def main(parameters):
    writepath = parameters.get("writepath")
    ipfile = parameters.get("ipfile")
    port = parameters.get("port")
    n = 100
    perfileN = 100000
    if not os.path.exists(writepath):
        os.makedirs(writepath)
    with open(ipfile,'r') as fr:
        lines = fr.readlines()
        write_lines = []
        x = 1
        writefile = writepath+"hello.json"
        for i,ip in enumerate(lines):
            write_lines.append(ip.strip())
            if i%perfileN==0:
                writefile = writepath + str(x) + ".json"
                x += 1
            if i%n==0 and i!=0:
                data2json(getdata(write_lines,port),writefile)
                write_lines = []
        if len(write_lines)!=0:
            data2json(getdata(write_lines, port), writefile)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="scannode parameter description")
    parser.add_argument("--writepath")
    parser.add_argument("--ipfile")
    parser.add_argument("--port")
    args = parser.parse_args(sys.argv[1:])
    parameters = vars(args)
    main(parameters)