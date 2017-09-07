import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '208',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '__jsluid=7ffac4ffdbe15c9adbd68bff8333bab0; bdshare_firstime=1501126794292; __jsl_clearance=1504692383.597|0|vsdnQfeVqeRmDhL7jUh%2FqHuTBkk%3D; JSESSIONID=64CF0251F3A03A9BD229DC5639333CC3',
        'Host': 'www.cnvd.org.cn',
        'Origin': "http://www.cnvd.org.cn",
        'Pragma':'no-cache',
        'Referer':"http://www.cnvd.org.cn/flaw/list.htm?flag=true",
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

    }
    data = {
        'offset':0,
        'max':100,
        'keyword':'Rockwell',
        'condition':'0',
        'keywordFlag':'0',
        'cnvdId':'',
        'cnvdIdFlag':'0',
        'baseinfoBeanbeginTime':'',
        'baseinfoBeanendTime':'',
        'baseinfoBeanFlag':'0',
        'refenceInfo':'',
        'referenceScope':'-1',
        'manufacturerId':'-1',
        'categoryId':'-1',
        'editionId':'-1',
        'causeIdStr':'',
        'threadIdStr':'',
        'serverityIdStr':'',
        'positionIdStr':''
    }
    iheaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',


        'Cookie': '__jsluid=7ffac4ffdbe15c9adbd68bff8333bab0; bdshare_firstime=1501126794292; __jsl_clearance=1504692383.597|0|vsdnQfeVqeRmDhL7jUh%2FqHuTBkk%3D; JSESSIONID=64CF0251F3A03A9BD229DC5639333CC3',
        'Host': 'www.cnvd.org.cn',

        'Pragma':'no-cache',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

    }
    q = requests.post("http://www.cnvd.org.cn/flaw/list.htm?flag=true",data=data,headers=headers)
    bs = BeautifulSoup(q.text,'lxml-xml').find_all("tr")
    lines = []
    print(q.status_code)
    for i in bs:
        j =i.find_all("td")
        if len(j)==0:
            continue
        p = j[0].find("a")
        title = p.get("title")
        href = str(p.get("href"))
        cnvd = href.split("/")[-1]
        rank = j[1].text.strip()
        iq = requests.get("http://www.cnvd.org.cn"+href,headers=iheaders)
        print(iq.status_code)
        ibs = BeautifulSoup(iq.text,'lxml').find_all("tr")
        cve = "-"
        for ii in ibs:
            ij = ii.find_all("td")
            if len(ij) == 2:
                if ij[0].text == "CVE ID":
                    cve = ij[1].text.strip()

        lines.append(str(cnvd)+'\t'+cve+"\t"+str(title)+"\t"+str(rank)+"\t"+"\n")
    # print(lines)
    with open("E:/text.txt","w",encoding="utf8") as fw:
        fw.writelines(lines)
