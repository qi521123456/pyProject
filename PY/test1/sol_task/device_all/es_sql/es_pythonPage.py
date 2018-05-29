from elasticsearch import Elasticsearch
import elasticsearch
from bs4 import BeautifulSoup
import xlwt
from openpyxl import Workbook
es = Elasticsearch(hosts=['192.168.205.169:8200'],http_auth=('elastic','elastic'))
q = '''{
    "size": 1000,
    "query": {
        "bool":{"should":[
                    {"match_phrase":{"body":"电力"}},
                    {"match_phrase":{"body":"电能"}}
                ]
            }
        }
    }'''
file = 'E:/electricity2.csv'
def queryDate():
    doc_count = 0
    try:
        querydata = es.search(index='python_page', doc_type='my_type', scroll='1m', timeout='5s',body=q)
        mdata = querydata.get("hits").get("hits")
        if not mdata:
            print("查询失败")
            return
        data = [d.get("_source") for d in mdata]
        sid = querydata['_scroll_id']
        while True:
            rs = es.scroll(scroll_id=sid, scroll='10s')
            temp = rs.get("hits").get("hits")
            if not temp:
                break
            data += [d.get("_source") for d in temp]
            write2file(file,data)
            doc_count+=data.__len__()
            print("写完成 · %s · 条"%doc_count)
            data=[]
    except Exception as ex:
        print(ex)
        return

def write2file(file,data):
    counttitle = 0
    with open(file,'a+',encoding='utf8') as fw:
        for i in data:
            try:
                ip = i.get('ip')
                port = i.get('port')
                head = i.get('head')
                body = i.get('body')
                title = None
                if head:
                    title = head.get('title')
                if not title:
                    bs = BeautifulSoup(body)
                    title = bs.title.text
                if title:
                    counttitle += 1
                    fw.write("%s\t%s\t%s\t\t%s\n"%(ip,port,str(title).strip(),str(body).replace('\r','-').replace('\n','-').replace('\t','-')))
            except Exception as e:
                #print(e)
                pass
    print("有title的 · %s ·条"%counttitle)

def write2xls():
    wb = Workbook()
    wb.create_sheet()
    sheet = wb.active
    sheet.title = 'elec'
    with open(file,'r',encoding='utf8') as fr:
        for index_line,line in enumerate(fr):
            try:
                sss = line.split("\t")
                for j in range(4):
                #for i,sssi in enumerate(sss):
                    sj = sss[j]
                    if j==3:
                        sj = "".join(sss[4])
                    #sheet.write(index_line, j, sj)
                sheet.append(sss)
            except:
                pass

    wb.save('E:/elec.xlsx')

if __name__ == '__main__':
    write2xls()