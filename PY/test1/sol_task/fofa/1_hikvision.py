import json,ijson
import pymysql
import socket,struct
import sys,os,shutil
import xml.etree.cElementTree as ET

def getinfo(path='D:/test_e/header/hikvision.json'):
    try:
        with open(path, 'rb') as f:
            data = json.loads(f.read().decode())['hits']['hits']
            l = _jsonData(data)
            f.close()
    except MemoryError:
        with open(path, 'r', encoding='utf-8') as f:
            data = ijson.items(f, 'hits.hits.item')
            l = _jsonData(data)
            f.close()
    return l

def _jsonData(data):
    l = list()
    for row in data:
        d = dict()
        ip = row['_source']['ip']
        port = ''
        _id = row['_id']
        createtime = row['_source']['lastchecktime']
        info = 'None'  # TODO find device info
        index = _id.rfind(':')
        if 'port' in row['_source']:
            port = str(row['_source']['port'])
        elif index != -1:  # 有个别没port，但id后有端口
            port = _id[index + 1:]
        if not port.isdigit():
            port = "80"
        d['ip'] = ip
        d['port'] = port
        d['createtime'] = createtime
        d['info'] = info
        l.append(d)
    return l

def _mysql_connect():
    connection = pymysql.connect(host='10.0.1.188',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='sol_daily',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def to_db(l,vendor):
    res = list()
    con = _mysql_connect()
    try:
        with con.cursor() as cursor:
            for d in l:
                ip = d['ip']
                packedIP = socket.inet_aton(ip)
                iplong = str(struct.unpack('!L', packedIP)[0])
                sql = "SELECT country, province, city FROM ip_ipipnet where ip_from < "+iplong+" and ip_to > "+iplong+""
                cursor.execute(sql)
                try:
                    location = cursor.fetchall()[0]
                except IndexError:
                    location = {'country': '*', 'city': '*', 'province': '*'}
                d.update(location)
                insertsql = 'INSERT INTO fofa (create_time, device_ip, device_port, device_country, device_province,' \
                            'device_city, vendor, device_info) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s")'\
                            % (d['createtime'],str(d['ip']),str(d['port']),str(d['country']),str(d['province']),
                               str(d['city']),str(vendor),str(d['info']))
                # print(insertsql)
                cursor.execute(insertsql)
                con.commit()
                res.append(d)
                sys.stdout.write('\r%s%%' % str(round(len(res)*100/len(l),2)))
                sys.stdout.flush()
            cursor.close()
    finally:
        con.close()
    return res

def _check_from_xml(path='D:/res.xml'):
    checkedip = list()
    tree = ET.parse(path)
    for child in tree.getroot().findall('host'):
        ip = child.find('address').attrib['addr']
        e = None
        try:
            e = child.find('ports').find('port').find('script').find('elem').text
        except AttributeError:
            pass
        if not e is None:
            checkedip.append(ip)
    return checkedip

def alter_check(ips):
    con = _mysql_connect()
    try:
        with con.cursor() as cursor:
            for ip in ips:
                update_sql = "UPDATE fofa SET checked = 1 WHERE device_ip = '"+ip+"'"
                cursor.execute(update_sql)
                con.commit()
            cursor.close()
    finally:
        con.close()

def _getPortIps_fromInfo(info):
    ips = dict()
    for data in info:
        port = data['port']
        ip = data['ip']
        if not port in ips:
            ips[port] = [ip]
        else:
            ips[port].append(ip)
    return ips
def scanIps(info,path='D:/_scan/',script='D:/HTTP.nse'):
    checkedIps = list()
    xmlPath = path+'xml/'
    if not os.path.isdir(path):
        os.mkdir(path)
        os.makedirs(xmlPath)
    ips = _getPortIps_fromInfo(info)
    for (port,ip) in ips.items():
        with open(path+port+'.txt','w') as fw:
            fw.writelines([line+'\n' for line in ip])
            fw.close()
    for ipfile in os.listdir(path):
        port = ipfile.split('.')[0]
        if not port.isdigit():
            continue
        cmd = "nmap -Pn --script %s -p %s -iL %s -oX %s" % (script,
        port, path + ipfile, xmlPath + port + '.xml')
        # print(cmd)
        os.system(cmd)
    for xmlfile in os.listdir(xmlPath):
        checkedIps.extend(_check_from_xml(xmlPath+xmlfile))
    #shutil.rmtree(path)
    return checkedIps
##############################################################################################################
def uncheck2mysql(jsonPath):
    for jsonfile in os.listdir(jsonPath):
        vendor = jsonfile.split('.')[0]
        if jsonfile.split('.')[1] != 'json':
            continue
        print(jsonfile)
        info = getinfo(jsonPath+jsonfile)
        to_db(info, vendor)
def addCheck(jsonPath):
    info = getinfo(jsonPath)
    checkIps = scanIps(info)
    alter_check(checkIps)
if __name__ == "__main__":
    uncheck2mysql("D:/test_e/title/")


