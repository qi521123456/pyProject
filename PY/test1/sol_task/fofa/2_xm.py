import ijson
import json
import pymysql
import sys,os
import socket,struct

def reduceinfo(infile='D:/test_e/jsonReduction/B-LINK-link.json',outfile ="D:/B-Link.json"):
    l = list()
    with open(infile, 'r', encoding='utf-8') as f:
        data = ijson.items(f, 'hits.hits.item')
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
    with open(outfile,'w') as fw:
        fw.write(str(l))
    return l

def getinfo2(filename="D:/xm.json"):
    with open(filename,'r') as f:
        l = eval(f.read())
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

def testIjson():
    path = 'D:/test_e/jsonReduction/B-LINK-link.json'
    with open(path, 'r',encoding='utf-8') as f:
        data = ijson.items(f,'hits.hits.item')
        f.close()
        print(next(data))

if __name__ == "__main__":
    # info = getinfo2("D:/B-Link.json")
    # to_db(info, "B-Link")
    testIjson()

