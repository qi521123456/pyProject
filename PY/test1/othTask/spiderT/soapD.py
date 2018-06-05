import zeep,socket
import threadpool
from netaddr import IPNetwork

def wppService(ip):
    wsdl2 = 'http://%s:7087/wpp/WPPService?wsdl'%ip
    try:
        client = zeep.Client(wsdl=wsdl2)
        reqinfo = '{"substationInfo":{"Zone3":{"fileDownloadFail":2,"fileSendFail":1,"isolationFail":1,"z3_serialport_status":0,"zx_isolation_status":2},"fCapacity":100.0,"licenseID":"3780-9891-5296-0368-2248","szSubStationID":"NRS00211","tSubstationReportTime":1526834760}}'
        res = client.service.Request("ReportStatus", reqinfo)
        if res.find('ReplyInfo')!=-1:
            return True
    except:
        pass
    return False

def openIps(path,port):
    '''
    :param path: ip文件
    :param port: 开放端口
    :return: 开放#port的ip们
    '''
    ips = []
    with open(path,'r') as fr:

        for line in fr:
            for ip in IPNetwork(line.strip()):
                ip = ip.__str__()
                try:
                    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sk.settimeout(0.01)
                    sk.connect((ip, port))
                    ips.append(ip)
                    print('------------%s--open'%ip)
                except Exception as e:
                    pass
                    # print(e)
                    # print('close %s'%ip)
                finally:
                    sk.close()
    return ips
if __name__ == '__main__':
    pool = threadpool.ThreadPool(10)

    ips = openIps('D:/320000.txt',7087)
    print(len(ips))
    with open('D:/7087.txt','a+') as fw:
        for ip in ips:
            fw.write(ip+'\n')