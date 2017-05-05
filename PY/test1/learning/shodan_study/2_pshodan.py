import requests
from bs4 import BeautifulSoup
import re
header = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
          'cookie':r'__cfduid=d3c474a331a92e2947c1f1ee8228090b81475030533; AJSTAT_ok_times=2;'
                   r' polito="600739f9e6da0077937c8e60fefa585058c604af57eb5a9ce449853ebf8ae5a5!";'
                   r' _LOCALE_=en; session="29981e24241882387285b8a91a6009fd880e7c63gAJVQDUwNTk1ZG'
                   r'RjZWEzMDBkZTBiMTFhNjZkM2M2Y2JlYzBjY2MwZmYzMTZiMWUzODU5YTZkNzY3YjcwMWVlOTA3YjhxAS4\075";'
                   r' _ga=GA1.2.1971536465.1475030534'}
def get_ips(params):
    ips = []
    for i in range(6):
        dip = []
        response = requests.Session().get('https://www.shodan.io/search?query='+params+'&page='+str(i),headers=header)
        soup = BeautifulSoup(response.text,'lxml')
        iplist = soup.find_all("div",attrs={'class': "ip"})
        for ipstr in iplist:
            dip.append(ipstr.a.string)
        ips.extend(dip)
    return ips


with open('D:/ips.txt', 'w') as fw:
    for data in get_ips("port:102"):
        fw.write(data + '\n')
