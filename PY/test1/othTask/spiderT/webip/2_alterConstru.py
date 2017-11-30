import os

import datetime,ijson
from bs4 import BeautifulSoup
import threading
import gc
def splitf(file,target,n):
    if not os.path.exists(target):
        os.makedirs(target)
    with open(file,'r',encoding='utf8') as fr:
        # lines = fr.readlines() # 大文件不适用
        for i,line in enumerate(fr):
            fw = open(target+str(i%n)+".txt",'a+',encoding='utf8')
            fw.write(line)
            fw.close()
def splitByLines(file,target,lines):
    if not os.path.exists(target):
        os.makedirs(target)
    with open(file,'r',encoding='utf8') as fr:
        for i,line in enumerate(fr):
            fw = open(target+str(i//lines)+".txt",'a+',encoding='utf8')
            fw.write(line)
            fw.close()
def alterCon(src,dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for f in os.listdir(src):
        if f[-4:]!="json":
            continue
        print(f)
        path = os.path.join(src,f)
        try:
            fw = open(os.path.join(dst,f),'w',encoding='utf8')
            with open(path,'r',encoding='utf8') as fr:

                for line in fr:
                    if line.strip()=='':
                        continue

                    # try:
                    idata = _repl(eval(line.strip()))
                    # except:
                    #     print(line)
                    #     exit(0)
                    #print(idata)
                    fw.write(str(idata)+'\n')
                    # gc.collect()
            fw.close()
        except MemoryError:
            print("memory error: "+f)


def _cdata(s):
    # print(type(s))
    data = {}
    for k in s:
        if k=='header':
            q_header = {}
            qh = dict(s[k])
            for i in qh:
                if i is not None and qh[i] is not None:
                    if i=="Last-Modified" or i=="Date" or i=="Expires":
                        s = qh[i]
                        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
                        try:
                            d = datetime.datetime.strptime(s, GMT_FORMAT)
                            if not isinstance(d,datetime.datetime):
                                continue
                        except:
                            continue
                    try:
                        if len(i)<3 or type(int(i))==int:
                            continue
                    except:
                        pass
                    q_header[i.strip('').strip('.').replace('.','-').lower()] = qh[i].strip('').strip('.')
            data['server'] = q_header
        elif k=='content':
            if s[k] != '':
                try:
                    soup = BeautifulSoup(s[k], from_encoding='utf8')
                    head = {}
                    head['title'] = soup.title.string
                    for child in soup.head.children:
                        if child.name == "meta":
                            attr = child.attrs
                            name = attr.get('name')
                            if name is not None and name.strap()!="" and name.find("time")==-1:
                                head[_keyFormat(attr['name']).lower()] = attr['content']
                    data['head'] = head
                    body = ""
                    for bodystr in soup.body.stripped_strings:
                        body += "\t" + bodystr
                    data['body'] = body.strip()
                except:
                    data['head'] = ''
                    data['body'] = s[k]
            else:
                data['head'] = ''
                data['body'] = ''
        else:
            data[k] = s[k]
    return data

def _repl(s):
    #print(type(s))
    if type(s) is not dict:
        print(s)
        return {}
    data = {}
    for k in s:
        if k=='server' or k=='head':
            q_header = {}
            qh = dict(s[k])
            for i in qh:
                if i is not None and qh[i] is not None:
                    if i=="Last-Modified" or i=="Date":
                        st = qh[i]
                        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
                        try:
                            d = datetime.datetime.strptime(st, GMT_FORMAT)
                            if not isinstance(d,datetime.datetime):
                                continue
                        except:
                            continue
                    try:
                        if len(i)<3 or type(int(i))==int:
                            continue
                    except:
                        pass
                    q_header[i.strip('').strip('.').replace('.','-').lower()] = qh[i].strip('').strip('.')
            data[k] = q_header
        else:
            #print(type(s))
            data[k] = s[k]
    return data
def _keyFormat(v):
    return v.strip('').strip('.').replace('.','-')

if __name__ == '__main__':
    # splitByLines("E:/camera2.txt","E:/camera/2/",1000)
    # l = ["httpjson_1013","httpjson_1017","httpjson_1025","httpjson_1010"]
    # for j in l:
    i = str("hj1109")
    src = "E:/TASK/"+i+"/"
    dst = 'E:/afterprocess/'+i+"/"
    thread = threading.Thread(target=alterCon,args=(src,dst,))
    thread.start()
