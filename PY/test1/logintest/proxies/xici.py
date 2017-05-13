## http ，http://www.xicidaili.com/wt/
import requests,re
from bs4 import BeautifulSoup


def get_ips(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
    headers = {'User-Agent': user_agent}
    html_doc = requests.get(url,headers=headers)  # 加useragent模拟网页
    # path = "D:/xicihttp.html"
    # with open(path,'rb') as f:
    #     html_doc = f.read().decode()
    #
    #     f.close()
    #
    soup = BeautifulSoup(html_doc.text,'lxml')

    proxies = []
    #匹配带有class属性的tr标签
    taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})
    for trtag in taglist:
        tdlist = trtag.find_all('td')  #在每个tr标签下,查找所有的td标签
        if len(tdlist) <1:
            continue
        # print(tdlist[1].string )  #这里提取IP值
        # print(tdlist[5].string )  #这里提取端口值
        if tdlist[5].string == "HTTP":
            proxies.append("http://"+tdlist[1].string+":"+tdlist[2].string)

    print(len(proxies))
    return proxies

def proxy_test(proxies):
    url = "http://httpbin.org/"
    usable_proxies = []
    for xy in proxies:
        proxy = {"http": xy}
        try:
            res = requests.get(url, proxies=proxy, timeout=0.5)
            if res.status_code == 200:
                print(xy)
                usable_proxies.append(proxy)
        except:
            pass
    return usable_proxies

def http_url(proUrl,n):
    # url:http://www.xicidaili.com/nn/1
    usable_proxies = []
    i = 6
    while i <= n:
        url = proUrl+str(i)
        proxies = get_ips(url)
        usable_proxies.extend(proxy_test(proxies))
        i += 1
    return usable_proxies

if __name__ == "__main__":
    # url = "http://www.xicidaili.com/"
    pro_url = "http://www.xicidaili.com/nn/"
    print(http_url(pro_url,50))

