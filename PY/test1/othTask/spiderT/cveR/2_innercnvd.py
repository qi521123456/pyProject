import requests
from bs4 import BeautifulSoup
headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',


        'Cookie': '__jsluid=c4d66f2f67ce26aee64d0268e1537751; bdshare_firstime=1504661817591; JSESSIONID=3BEC3C751A220D5F2372FB69712446C5; __jsl_clearance=1504689712.859|0|TicG2d1oqbHIbjVJTmoZAsNZivo%3D',
        'Host': 'www.cnvd.org.cn',

        'Pragma':'no-cache',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

    }

iq = requests.get("http://www.cnvd.org.cn/flaw/show/CNVD-2016-01451",headers=headers)
print(iq.status_code)
ibs = BeautifulSoup(iq.text,'lxml').find_all("tr")
for ii in ibs:
    ij = ii.find_all("td")
    if len(ij)==2:
        if ij[0].text == "CVE ID":

            print(ij[1].text)