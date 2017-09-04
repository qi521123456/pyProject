import json, io, threading
import pycurl
import sys
import argparse
import datetime


TABLES = ["service","subdomain"]
QUERYS = [
    {"name":"华为路由器","query":'{"bool":{"must":[{"time":"'+time+'"},{"header":"HuaweiHomeGateway"}]}}'},
    {"name":"Hikvision","query":'{"bool":{"must":[{"time":"'+time+'"},{"bool":{"should":[{"header":"Hikvision"},{"header":"_goaheadwebSessionId"},{"header":"DVRDVS-Webs"},{"bool":{"must":[{"body":"updateTips"},{"body":"doc/page/login.asp"}]}}]}}]}}'},
    {"name":"DVR_Streamer","query":'{"bool":{"must":[{"time":"'+time+'"},{"bool":{"should":[{"header":"DVR Streamer"},{"title":"DVR Streamer"},{"body":"DVR Streamer"}]}}]}}]}}'},
    {"name":"mikrotik","query":'{"bool":{"must":[{"time":"'+time+'"},{"title":"RouterOS"},{"body":"mikrotik"}]}}'},
    {"name":"雄迈","query":'{"bool":{"must":[{"time":"'+time+'"},{"header":"Server uc-httpd 1.0.0"}]}}'},
    {"name":"D-Link_DCS","query":'{"bool":{"must":[{"time":"'+time+'"},{"bool":{"should":[{"header":"realm DCS"},{"title":"realm DCS"},{"body":"realm DCS"}]}}]}}'},
    {"name":"NETSurveillance","query":'{"bool":{"must":[{"time":"'+time+'"},{"title":"NETSurveillance"}]}}'},

]
class ESAgent():
    def __init__(self, baseURL, user=None, pwd=None):
        self.agent = pycurl.Curl()
        self.agent.setopt(pycurl.URL, baseURL)
        self.url = baseURL
        if user:
            if pwd:
                self.agent.setopt(pycurl.USERPWD, str(user) + ':' + str(pwd))
            else:
                self.agent.setopt(pycurl.USERNAME, str(user))
                # self.Search('')

    def Search(self, query):
        buf = io.BytesIO()
        self.agent.setopt(pycurl.WRITEFUNCTION, buf.write)
        if query:
            self.agent.setopt(pycurl.POST, True)
            self.agent.setopt(pycurl.POSTFIELDS, query)
        else:
            self.agent.setopt(pycurl.POST, False)
        self.agent.perform()
        res = buf.getvalue().decode()
        return res

    def changeURL(self, newURL):
        self.agent.setopt(pycurl.URL, newURL)
        self.url = newURL

    def fofa2es(self, query):
        qdic = query.split()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="fofa_es parameter description")
    parser.add_argument("--table")
    args = parser.parse_args(sys.argv[1:])
    parameters = vars(args)
    agent = ""
    res = ""
    if parameters.get("table") != None:
        # agent = ESAgent("http://10.166.77.117:9200/fofa_new/" + parameters.get("table") + "/_search?pretty",
        #                 "fofa_guangpu_reader_gk", "123456")
        agent = ESAgent("http://192.168.120.33:9200/norn/" + parameters.get("table") + "/_search?pretty","norn_admin","123456")
    else:
        print("input the table name with --table")
        exit()
    # port_list = [102,502,161,503,44818,1911,2222,21,9600,5007,5006,47808,37777]
    now = datetime.datetime.now()
    keywords = ["Huawei", "ZTE", "TP-LINK", "B-LINK", "B-link", "Ruijie", "Cisco", "Maipu", "ralink", "TOTOLINK",
                "D-Link", "Netgear", "Juniper", "Linksys", "Siemens", "Rockwell", "Schneider", "ABB", "H3C", "Dahua",
                "GeoVision", "Hikvision"]

    for port in range(0, 11):

        port = datetime.timedelta(days=port)
        port = now - port
        port = port.strftime("%Y-%m-%d")
        query = '''{"size":10,"query":{
                                    "bool":{
                                            "must":[
                                                    {"match":{"protocol_transport":"TCP"}},

                                                    {"bool":{"should":[{"match":{"port":103}},{"match":{"port":102}}]}},
                                                    {"match":{"protocol_application":"S7Comm"}}

                                            ]
                                    }
                            }
                 }'''
        #print(str(query))
        res = agent.Search(str(query))
        a = json.loads(res)
        if a.get("hits") is None:
            continue
        b = a.get("hits").get("hits")
        if len(b) == 0 or b is None:
            continue
        else:
            print("------------------------------writefile")
            fp = open("E:/fofa/" + str(port) + ".txt", "a+", encoding="utf-8")
            for c in b:
                d = str(c.get("_source"))
                fp.write(d + "\n")
            fp.close()
    # for k in keywords:
    #     for port in range(0, 1001):
    #         print(port)
    #         port = datetime.timedelta(days=port)
    #         port = now - port
    #         port = port.strftime("%Y-%m-%d")
    #         # query = '{"size":10000,"query":{"match":{"' + "time" +'":"' + port + '"}}}'
    #         query_1 = '{"size":10000,"query":{"bool":{"should":[{"match":{"time":"' + port + '"}},{"match":{"header":"' + k + '"}}]}}}'
    #         print(query_1)
    #         res = agent.Search(query_1)
    #         a = json.loads(res)
    #         b = a.get("hits").get("hits")
    #         if len(b) == 0:
    #             continue
    #         else:
    #             fp = open("D:/fofa/" + str(port) + "-" + k + ".txt", "a+", encoding="utf-8")
    #             for c in b:
    #                 d = str(c.get("_source"))
    #                 fp.write(d + "\n")
    #             fp.close()
    print("OK!")