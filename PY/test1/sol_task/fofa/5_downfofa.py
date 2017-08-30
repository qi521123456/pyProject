import json, io, threading
import pycurl
import sys
import argparse
import datetime

TABLES = ["service", "subdomain"]
PATH = "E:/fofa/"


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
    now = datetime.datetime.now()
    for table in TABLES:
        agent = ESAgent("http://10.166.77.117:9200/fofa_new/" + table + "/_search?pretty","fofa_guangpu_reader_gk", "123456")
        # agent = ESAgent("http://192.168.120.33:9200/norn/" + parameters.get("table") + "/_search?pretty","norn_admin","123456")
        for x in range(0, 201):
            time = datetime.timedelta(days=x)
            time = now - time
            time = time.strftime("%Y-%m-%d")
            querys = [
                {"name": "华为路由器",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"header":"HuaweiHomeGateway"}]}}'},
                {"name": "Hikvision",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"bool":{"should":[{"header":"Hikvision"},{"header":"_goaheadwebSessionId"},{"header":"DVRDVS-Webs"},{"bool":{"must":[{"body":"updateTips"},{"body":"doc/page/login.asp"}]}}]}}]}}'},
                {"name": "DVR_Streamer",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"bool":{"should":[{"header":"DVR Streamer"},{"title":"DVR Streamer"},{"body":"DVR Streamer"}]}}]}}]}}'},
                {"name": "mikrotik",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"RouterOS"},{"body":"mikrotik"}]}}'},
                {"name": "雄迈",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"header":"Server uc-httpd 1.0.0"}]}}'},
                {"name": "D-Link_DCS",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"bool":{"should":[{"header":"realm DCS"},{"title":"realm DCS"},{"body":"realm DCS"}]}}]}}'},
                {"name": "NETSurveillance",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"NETSurveillance"}]}}'},
                {"name": "大华摄像头",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"bool":{"should":[{"header":"Dahua Technology"},{"title":"Dahua Technology"},{"body":"Dahua Technology"}]}}]}}]}}'},
                {"name": "ZyXEL", "query": '{"bool":{"must":[{"time":"' + time + '"},{"body":"Forms/rpAuth_1"}]}}'},
                {"name": "Ruckus",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"bool":{"should":[{"title":"Ruckus Wireless Admin"},{"body":"mon. Tell me your username"}]}}]}}]}}'},
                {"name": "TP-LINK无线路由器",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"header":"TP-LINK Wireless"}]}}'},
                {"name": "Avtech",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"bool":{"should":[{"header":"Avtech"},{"title":"Avtech"},{"body":"Avtech"}]}}]}}]}}'},
                {"name": "eagleeyescctv",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"bool":{"should":[{"body":"/nobody/loginDevice.js"},{"body":"IP Surveillance for Your Life"}]}}]}}]}}'},
                {"name": "GeoVision",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"bool":{"should":[{"header":"GeoHttpServer for webcams	GeoHttpServer"},{"title":"GeoHttpServer for webcams	GeoHttpServer"},{"body":"GeoHttpServer for webcams	GeoHttpServer"}]}}]}}]}}'},
                {"name": "中兴路由器",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"header":"Server: Mini web server 1.0 ZTE corp 2005."}]}}'},
                {"name": "arrisi_Touchstone",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"bool":{"should":[{"title":"ouchstone Status"},{"body":"passWithWarnings"}]}}]}}]}}'},
                {"name": "edvr", "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"edvs/edvr"}]}}'},
                {"name": "NetDvrV3", "query": '{"bool":{"must":[{"time":"' + time + '"},{"body":"objLvrForNoIE"}]}}'},
                {"name": "AVCON6",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"bool":{"should":[{"title":"AVCON6"},{"body":"language_dispose.action"}]}}]}}]}}'},
                {"name": "Mvpower", "query": '{"bool":{"must":[{"time":"' + time + '"},{"header":"Server: JAWS"}]}}'},
                {"name": "MOBOTIX_Camera",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"bool":{"should":[{"header":"MOBOTIX Camera User"},{"title":"MOBOTIX Camera User"},{"body":"MOBOTIX Camera User"}]}}]}}]}}'},
                {"name": "ECOR", "query": '{"bool":{"must":[{"time":"' + time + '"},{"header":"ECOR264"}]}}'},
                {"name": "Polycom",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"Polycom"},{"body":"kAllowDirectHTMLFileAccess"}]}}'},
                {"name": "dd-wrt",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"body":"dd-wrt.com"},{"body":"load average"}]}}'},
                {"name": "h3c路由器",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"Web user login"},{"body":"nLanguageSupported"}]}}'},
                {"name": "Linksys_SPA_Configuration ",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"Linksys SPA Configuration"}]}}'},
                {"name": "Scientific-Atlanta_Cable_Modem",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"Scientific-Atlanta Cable Modem"}]}}'},
                {"name": "AirLink_modem",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"header":"Modem@AirLink.com"}]}}'},
                {"name": "nvdvr", "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"XWebPlay"}]}}'},
                {"name": "D-Link_VoIP_Wireless_Router",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"D-Link VoIP Wireless Router"}]}}'},

                {"name": "DI-804HV", "query": '{"bool":{"must":[{"time":"' + time + '"},{"header":"DI-804HV"}]}}'},
                {"name": "MOBOTIX_Camera",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"header":"MOBOTIX Camera"}]}}'},
                {"name": "锐捷NBR路由器",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"body":"free_nbr_login_form.png"}]}}'},
                {"name": "iDVR",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"header":"Server: iDVRhttpSvr"}]}}'},
                {"name": "jcg无线路由器",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"Wireless Router"},{"body":"http://www.jcgcn.com"}]}}'},
                {"name": "Wimax_CPE",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"Wimax CPE Configuration"}]}}'},
                {"name": "Aethra_Telecommunications_Operating_System",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"header":"atos"}]}}'},
                {"name": "jcg无线路由器",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"Wireless Router"},{"body":"http://www.jcgcn.com"}]}}'},
                {"name": "佳能网络摄像头(Canon Network Cameras)",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"body":"/viewer/live/en/live.html"}]}}'},
                {"name": "Cisco_Cable_Modem",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"Cisco Cable Modem"}]}}'},
                {"name": "Macrec_DVR", "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"Macrec DVR"}]}}'},
                {"name": "EdmWebVideo",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"EdmWebVideo"}]}}'},
                {"name": "Comcast_Business_Gateway",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"body":"Comcast Business Gateway"}]}}'},
                {"name": "DVR_camera",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"DVR WebClient"}]}}'},
                # OnSSI_Video_Clients title="OnSSI Video Clients" || body="x-value=\"On-Net Surveillance Systems Inc.\""
                {"name": "OnSSI_Video_Clients",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"bool":{"should":[{"title":"OnSSI Video ClientsOnSSI Video Clients"},{"body":"x-value=\"On-Net Surveillance Systems Inc.\""}]}}]}}]}}'},
                {"name": "dasannetworks",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"body":"clear_cookie(\"login\");"}]}}'},
                {"name": "TRSMAS", "query": '{"bool":{"must":[{"time":"' + time + '"},{"header":"X-Mas-Server"}]}}'},
                {"name": "海康威视iVMS",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"body":"g_szCacheTime"},{"body":"iVMS"}]}}'},
                {"name": "Motorola_SBG900",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"Motorola SBG900"}]}}'},
                {"name": "techbridge",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"body":"Sorry,you need to use IE brower"}]}}'},
                {"name": "ZTE_MiFi_UNE",
                 "query": '{"bool":{"must":[{"time":"' + time + '"},{"title":"MiFi UNE 4G LTE"}]}}'}

            ]
            for qs in querys:
                query = '{"size:10000","query":' + qs.get('query') + '}'
                #print(query)

                res = agent.Search(str(query))
                a = json.loads(res)
                if a.get("hits") is None:
                    continue
                b = a.get("hits").get("hits")
                if len(b) == 0 or b is None:
                    continue
                else:
                    fp = open(PATH + table +"/"+qs.get('name')+"/"+str(time) + ".txt", "a+", encoding="utf-8")
                    for c in b:
                        d = str(c.get("_source"))
                        fp.write(d + "\n")
                    fp.close()
    print("OK!")