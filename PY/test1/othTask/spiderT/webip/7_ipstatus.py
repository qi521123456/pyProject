import requests

def ipport(ip):
    urls = ["http://%s"%ip,"https://%s"+ip,"http://%s:8080"%ip]
    for url in urls:
        try:
            response = requests.get(url, timeout=0.05)
            status = response.status_code
            if status==200:
                # contain = response.text.find("WebAccess")
                # print(contain)
                # if contain!=-1:
                #     contain = "包含 WebAccess"
                # else:
                #     contain = "不含 WebAccess"
                # return "通",contain
                return url
        except:
            return None
    return None

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
    with open('/home/lmqdcs/wor/ip-url.txt','a+') as fw:
        with open('/home/lmqdcs/wor/ip-validate.txt','r') as fr:
            for line in fr:
                pp = line.strip()
                res = ipport(pp)
                if res:
                    fw.write(pp+"\t"+res+"\n")

