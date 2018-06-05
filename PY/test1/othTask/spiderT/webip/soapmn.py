import zeep
import json
from zeep import xsd
def wpp():
    wsdl = 'http://web.nwp-nrec.cn:7087/wpp/WPPService?wsdl'
    wsdl2 = 'http://183.207.177.76:7087/wpp/WPPService?wsdl'
    client = zeep.Client(wsdl=wsdl2)
    with client.options(timeout=1):
        print(client)
    print(1)
    # print(client.namespaces)
    reqinfo = '{"substationInfo":{"Zone3":{"fileDownloadFail":2,"fileSendFail":1,"isolationFail":1,"z3_serialport_status":0,"zx_isolation_status":2},"fCapacity":100.0,"licenseID":"3780-9891-5296-0368-2248","szSubStationID":"NRS00211","tSubstationReportTime":1526834760}}'
    res = client.service.Request("ReportStatus",reqinfo)
    print(type(res),res.find('ReplyInfo'))
    transport = zeep.Transport()
    head = {'ns0': 'http://www.nrec.com/wpp', 'xsd': 'http://www.w3.org/2001/XMLSchema'}

    a = '''<SOAP-ENV:Body>
        <ns1:RequestMessageType>
            <FunctionType>
                ReportStatus
                </FunctionType>
            <RequestInfo>
                 {"substationInfo":{"Zone3":{"fileDownloadFail":2,"fileSendFail":1,"isolationFail":1,"z3_serialport_status":0,"zx_isolation_status":2},"fCapacity":100.0,"licenseID":"3780-9891-5296-0368-2248","szSubStationID":"NRS00211","tSubstationReportTime":1526834760}}
                </RequestInfo>
            </ns1:RequestMessageType>
        </SOAP-ENV:Body>
    '''
    b = '''<?xml version="1.0" encoding="UTF-8"?>
        <SOAP-ENV:Envelope
        xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:ns1="http://www.nrec.com/wpp">
        <SOAP-ENV:Body>
            <ns1:RequestMessageType>
                <FunctionType>
                    ReportStatus
                    </FunctionType>
                <RequestInfo>
                     {"substationInfo":{"Zone3":{"fileDownloadFail":2,"fileSendFail":1,"isolationFail":1,"z3_serialport_status":0,"zx_isolation_status":2},"fCapacity":100.0,"licenseID":"3780-9891-5296-0368-2248","szSubStationID":"NRS00211","tSubstationReportTime":1526834760}}
                    </RequestInfo>
                </ns1:RequestMessageType>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>
    '''
    hb = {
        'Host': 'web.nwp-nrec.cn:7087',
        'User-Agent': 'gSOAP/2.8',
        'Content-Type': 'text/xml; charset=utf-8',
        'Content-Length': bytes(741),
        'Connection': 'close',
        'SOAPAction': "urn:Request"
    }
    # print(json.dumps(b))
    body = {"substationInfo":{"Zone3":{"fileDownloadFail":2,"fileSendFail":2,"isolationFail":1,"z3_serialport_status":1,"zx_isolation_status":2},"fCapacity":50.0,"licenseID":"6719-9038-7045-4580-8817","szSubStationID":"NRS00194","tSubstationReportTime":1526834760}}
    # res = transport.post("http://web.nwp-nrec.cn:7087/wpp/WPPService",message=json.dumps(b),headers=hb)
    # print(res.text)

def soapcom():
    wsdl = 'http://www.soapclient.com/xml/soapresponder.wsdl'
    client = zeep.Client(wsdl=wsdl)
    print(client.get_element('function'))
    print(client.service.Method1('Zeep', 'is cool'))

    header = xsd.Element(
        '{http://test.python-zeep.org}auth',
        xsd.ComplexType([
            xsd.Element(
                '{http://test.python-zeep.org}username',
                xsd.String()),
        ])
    )
    header_value = header(username='mvantellingen')
    # client.service.Method(_soapheaders=[header_value])
def airline():
    wsdl = 'http://ws.webxml.com.cn/webservices/DomesticAirline.asmx?wsdl'
    client = zeep.Client(wsdl=wsdl)

    ri = {'startCity':'北京', 'lastCity':'广州', 'theDate':'2017-05-22'}
    msg = client.create_message(client.service,'getDomesticAirlinesTime',startCity='北京',lastCity='广州',theDate='2017-05-22')
    print(msg)
    res = client.service.getDomesticAirlinesTime('北京','广州','2018-11-22')
    print(res)
    print(client.service.getDomesticCity())
    from lxml import etree
    print(etree.tostring(res._value_1).decode())
    for i in res._value_1.iter('Company'):
        print(i.text)

def portopen():
    import socket
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(0.01)
    try:
        sk.connect(('183.207.177.76',7087))
        print('Server port 80 OK!')
    except Exception:
        print('Server port 80 not connect!')
    sk.close()

def iptest():
    from netaddr import IPRange
    import socket
    with open('D:/jiangsuipduan.txt') as fr:

        with open('D:/jiangsuopen7087.txt','w') as fw:
            for line in fr:
                ils = line.strip().split(';')
                print(ils)
                for i in IPRange(ils[0],ils[1]):
                    print(i.__str__(),type(i.__str__()))
                    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sk.settimeout(0.01)
                    try:
                        sk.connect((i.__str__(), 7087))
                        fw.write(i+'\n')
                    except Exception as e:
                        print(e)
                        pass
                    sk.close()
if __name__ == '__main__':
    # portopen()
    iptest()
    # wpp()
    # airline()
