import requests
from bs4 import BeautifulSoup
def get_area(ip_address):
    """获取给定IP的地理位置
    :Paprameters:
       -ip_address：合法的ip地址
    """

    def extract(content):
        """从网页内容中提取地理位置
        :Parameters:
          --content：过滤后的网页内容
        """
        try:
            return content[content.find("：") + 1:len(content)].split(" ")[0]
        except:
            print("No area by given address")
            return "China"


    query = requests.get("http://www.ip138.com/ips138.asp", {"ip": ip_address})
    #print(query.url,eval(query.content))
    result = BeautifulSoup(query.content,'lxml').find("ul", {"class": "ul1"})
    print(result,"\n===\n",BeautifulSoup(query.content,'lxml'))
    return extract(result.find("li").text)


if __name__ == "__main__":
    print(get_area("183.55.116.95"))