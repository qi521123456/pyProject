import requests

def ipport(ip):
    urls = ["http://%s"%ip,"https://%s"+ip,"http://%s:8080"%ip]
    for url in urls:
        try:
            response = requests.get(url, timeout=1)
            status = response.status_code
            if status==200:
                contain = response.text.find("WebAccess")
                print(contain)
                if contain!=-1:
                    contain = "包含 WebAccess"
                else:
                    contain = "不含 WebAccess"
                return "通",contain
        except:
            status = "timeout"
    return "不通",""

def ipport2(ip,port):
    if port:
        url = "http://%s:%s"%(ip,port)
        try:
            response = requests.get(url, timeout=1)
            status = response.status_code
            if status==200:
                return "ok",'200'
            else:
                return "error",str(status)
        except:
            return "timeout",""
    else:
        urls = ["http://%s"%ip,"https://%s"+ip,"http://%s:8080"%ip]
        for url in urls:
            try:
                response = requests.get(url, timeout=1)
                status = response.status_code
                if status == 200:
                    return "ok", url
                else:
                    return "error", str(status)
            except:
                pass
        return "timeout", ""

if __name__ == '__main__':
    print("hello")
    with open('/home/mannix/Desktop/aaa.txt','w') as fw:
        with open('/home/mannix/Desktop/ip-port','r') as fr:
            for line in fr:
                pp = line.strip().split('\t')
                if len(pp)==2:
                    res = ipport2(pp[0],pp[1])
                else:
                    res = ipport2(pp[0],False)
                print(res)
                fw.write(pp[0]+"\t"+"\t".join(res)+"\n")

