import threading,requests
import sys,os
import xlwt
from bs4 import BeautifulSoup

def p2excel(txt,xls):
        try:
            fw = open(xls,"a+",encoding="utf-8")
            with open(txt,'r',encoding='utf-8') as fr:
                datalist = [["域名","IP","原标题","状态","现标题"]]
                fw.write("域名\tIP\t原标题\t状态\t现标题\n")
                for line in fr:
                    if line.strip()=='':
                        continue
                    idata = _ddata(line)
                    fw.write("\t".join(idata)+"\n")
                    #datalist.append(idata)
                    #print(idata)
                #w2sheet(xls,f[:-4],datalist)
            fw.close()
        except MemoryError:
            print("memory error: "+f)

def _ddata(line):
    data = eval(line.strip())
    host = data.get("host")
    origin_title = data.get("title").strip().replace(" ","_")
    ip = data.get("ip")
    port = data.get("port")
    if host is not None:
        if host.find("http") != -1:
            url = host
        else:
            url = "http://"+host
    elif ip is not None:
        if port is not None:
            url = "http://%s:%s"%(ip,str(port))
        else:
            url = "http://"+ip
    try:
        requests.session().keep_alive=False
        #requests.adapters.DEFAULT_RETRIES = 5
        q = requests.get(url,timeout=1)
        status = q.status_code
        # print(q.headers)
        soup = BeautifulSoup(q.content.decode("utf-8","ignore"))
        now_title = soup.title.string.replace(" ","_")
    except Exception as e:
        #print(e)
        status = ""
        now_title = ""

    return [host,ip,origin_title,str(status),now_title]
def w2sheet(xls,sheet,datalist):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheet)
    for i,d in enumerate(datalist):
        for j in range(0,5):
            try:
                ws.write(i,j,d[j])
            except:
                pass


if __name__ == '__main__':
    path = "E:/TASK/xf/xiaofang/"
    # wb = xlwt.Workbook()
    ths = []
    for f in os.listdir(path):
        if f[-3:]!="txt":
            continue
        print(f)
        thread = threading.Thread(target=p2excel,args=(os.path.join(path,f),os.path.join("E:/TASK/xf/res/",f[:-4]+".csv"),))
        thread.start()
        ths.append(thread)
    # for i in ths:
    #     i.join()
    #wb.save("E:/TASK/xf/xf.xls")
    #p2excel("E:/TASK/xf/xiaofang/","E:/TASK/xf/res/")
    #w2sheet("E:/a.xls","s1",[["22","11"],["33","44"]])
