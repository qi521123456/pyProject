
import requests
from bs4 import BeautifulSoup

def get_http(url):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Cookie": "Union=SID=155952&AllianceID=4897&OUID=baidu81|index|||; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; _abtest_userid=41d701c0-0139-4a1d-9d13-d742782bc75c; adscityen=Beijing; ASP.NET_SessionId=ekwz45rpi5gsqa3sroirwwu1; OID_ForOnlineHotel=15243109157814de2cs1524310929598102003992; _bfa=1.1524310915781.4de2cs.1.1524310915781.1524310915781.1.3; _bfs=1.3; HotelDomesticVisitedHotels1=429527=0,0,4.6,10066,/fd/hotel/g3/M06/D9/24/CggYGlXIGD-ANm7hABp2JMsP0jI411.jpg,&1816847=0,0,4.9,8316,/fd/hotel/g5/M08/8C/C1/CggYsFcrF_GAZHusAEAz_YYcL3E922.jpg,; _RF1=114.255.41.138; _RSG=sGqAlhsXxJ6N5D0hBLX.t8; _RDG=280bbb32bf1bee2e131d8265e5f2e71f70; _RGUID=64fb876a-ef2b-4436-8dfe-8552eb00d157; _ga=GA1.2.295167366.1524310919; _gid=GA1.2.1253274797.1524310919; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1524310997804%7D%5D; MKT_Pagesource=PC; _jzqco=%7C%7C%7C%7C1524310920072%7C1.2135537669.1524310919082.1524310931842.1524310997887.1524310931842.1524310997887.0.0.0.3.3; __zpspc=9.1.1524310919.1524310997.3%234%7C%7C%7C%7C%7C%23; _bfi=p1%3D102003992%26p2%3D102001%26v1%3D3%26v2%3D1",
        "Host": "hotels.ctrip.com",
        "If-Modified-Since": 'Thu, 01 Jan 1970 00":"00": "00 GMT',
        "Referer": 'http":"//hotels.ctrip.com/hotel/dianping/429527.html',
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
    }
    response = requests.get(url,headers)
    print(response.text,"-------")
    bs = BeautifulSoup(response.text)

    a = bs.find('div',{'class':'comment_detail_list'})
    b = a.find_all('div',{'class':'J_commentDetail'})
    for ib in b:
        print(ib.text)



if __name__ == '__main__':
    url = "http://hotels.ctrip.com/Domestic/tool/AjaxHotelCommentList.aspx?MasterHotelID=429527&hotel=429527&NewOpenCount=0&AutoExpiredCount=0&RecordCount=10066&OpenDate=2007-01-01&card=-1&property=-1&userType=-1&productcode=&keyword=&roomName=&orderBy=2&currentPage=2&viewVersion=c&contyped=0&eleven=d37c4ad64098286d0f0c47c0cff858849babec6a426aa2b197fca32730fac858&callback=CASqljPZbeQUAYkbR&_=1524311911091"
    get_http(url)