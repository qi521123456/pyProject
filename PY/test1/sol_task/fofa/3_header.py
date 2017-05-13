import json
import pymysql
import socket,struct
import sys,os,shutil
import xml.etree.cElementTree as ET


def getinfo(path='D:/test_e/header/hikvision.json'):
    l = list()
    with open(path, 'rb') as f:
        data = json.loads(f.read().decode())['hits']['hits']
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
                port = _id[index+1:]
            if not port.isdigit():
                port = "80"
            d['ip'] = ip
            d['port'] = port
            d['createtime'] = createtime
            d['info'] = info
            l.append(d)
        f.close()
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

def uncheck2mysql(jsonPath,vendor):
    info = getinfo(jsonPath)
    to_db(info,vendor)

def main(path="D:/test_e/header/"):
    for jsonfile in os.listdir(path):
        vendor = jsonfile.split('.')[0]
        if jsonfile.split('.')[1] != 'json':
            continue
        print(jsonfile)
        try:
            uncheck2mysql(path+jsonfile,vendor)
        except MemoryError:
            print(jsonfile,"memoryerror")


if __name__ == "__main__":
    main()

