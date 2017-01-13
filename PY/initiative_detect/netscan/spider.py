from urllib.request import  urlopen
from bs4 import BeautifulSoup

#http://ip.yqie.com/search.aspx?searchword=%E5%8C%97%E4%BA%AC
def spider_ip(root_url,page_count,province):
    start = 1
    url = None
    while start <= page_count:
        if start is 1:
            url = root_url
        else:
            index = url.find('searchword')