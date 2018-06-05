import requests
from bs4 import BeautifulSoup
import threading
def ipport(ip):
    urls = ["http://%s"%ip,"https://%s"+ip,"http://%s:8080"%ip]
    for url in urls:
        try:
            response = requests.get(url, timeout=0.5)
            status = response.status_code
            if status==200:
                return url
        except:
            pass
    return None

def get_ip_mask(path):
    maskIp = set()
    count = 0
    with open(path,'r') as fr:
        for line in fr:
            lastdot = line.rfind('.')
            if lastdot!=-1:
                count+=1
                maskIp.add(line[:lastdot+1])
    print(count,"  ",len(maskIp))
    return maskIp

def thread_mask(mask,write2):
    with open(write2,'a+') as fw:
        for i in range(1, 255):
            ip = mask+str(i)
            url = ipport(ip)
            print(ip+" : "+str(url))
            if url:
                fw.write(ip+"\t"+url+"\n")

def get_title(path,write2):
    with open(write2,'w',encoding='utf8') as fw:
        with open(path) as fr:
            for line in fr:
                ls = line.strip().split('\t')
                ip = ls[0]
                url = ls[1]
                try:
                    response = requests.get(url,timeout=1)
                    bs = BeautifulSoup(response.text)
                    title = bs.title.text
                    print(title)
                    fw.write(line.strip()+"\t"+title+"\n")
                except:
                    print(url)
if __name__ == '__main__':
    # maskips = get_ip_mask('D:/设备定位IP.TXT')
    # for i,mask in enumerate(maskips):
    #     # threadmask = threading.Thread(target=thread_mask,args=(mask,'D:/ip-url.txt',))
    #     # threadmask.start()
    #     print(i)
    #     thread_mask(mask,'D:/ip-url.txt')
    get_title('D:/ip-url.txt','D:/ip-url-title.txt')
    import datetime
    datetime.cm


