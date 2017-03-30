# coding=utf-8
import pymysql
import socket,struct
import sys
import json
TABLES = ['result_iec104', 'result_melsec_q_tcp', 'result_melsec_q_udp', 'result_modbus', 'result_moxa',
          'result_s7comm', 'result_snmp', 'result_http', 'result_fox', 'result_fins', 'result_ethernetip',
          'result_bacnet', 'result_cspv4', 'result_dahua', 'result_dnp3']
class DataPersistence:
    def __init__(self,host="10.0.1.199"):
        self.host = host
        self.tables = TABLES
    def __mysql_connect(self):
        connection = pymysql.connect(host=self.host,
                                     port=3306,
                                     user='root',
                                     password='123456',
                                     db='sol_daily',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    def to_result(self,tablename,data):
        if tablename not in self.tables:
            print("wrong table name！")
            return False
        con = self.__mysql_connect()
        try:
            with con.cursor() as cursor:
                count = 0
                for d in data:
                    ip = d['device_ip']
                    # q_sql = "SELECT device_ip FROM %s WHERE device_ip = '%s'" % (tablename,ip)
                    # cursor.execute(q_sql)
                    # if len(cursor.fetchall()) != 0:
                    #     continue
                    packedIP = socket.inet_aton(ip)
                    iplong = str(struct.unpack('!L', packedIP)[0])
                    sql = "SELECT country as device_country, province as device_province, city as device_city" \
                          " FROM ip_ipipnet where ip_from < " + iplong + " and ip_to > " + iplong + ""
                    cursor.execute(sql)
                    try:
                        location = cursor.fetchall()[0]
                        d.update(location)
                    except IndexError:
                        pass
                    d['task_id'] = -1
                    s1 = []
                    s2 = []
                    for k, v in d.items():
                        s1.append("`" + str(k) + "`")
                        s2.append("'" + str(v) + "'")
                    insert_sql = "INSERT INTO %s (%s) VALUES (%s)" % (tablename,','.join(s1), ','.join(s2))
                    # print(insert_sql)
                    cursor.execute(insert_sql)
                    con.commit()
                    count += 1
                    sys.stdout.write('\r%s%%' % str(round(count * 100 / len(data), 2)))
                    sys.stdout.flush()
        finally:
            con.close()
        return True
    def get_data(self,filename):
        res = []
        with open(filename,'r') as fr:
            for line in fr.readlines():
                d = json.loads(line)
                resd = {}
                sss = None
                if 'modbus' in d['opts']:
                    for i in d['opts']['modbus']:
                        for j in i['response']:
                            if j[0] == "Device Identification" and j[1].find('Error') == -1 and j[1].strip() != "":
                                sss = j[1]
                if sss:

                    print(d['ip_str'],sss)
                t = d['timestamp']
                timestamp = t[:t.find('.')].replace('T', ' ')
                ip = d['ip_str']
                port = d['port']
                location = d['location']

                resd['device_ip'] = ip
                resd['device_port'] = port
                resd['create_time'] = timestamp
                resd['latitude'] = location['latitude']
                resd['longitude'] = location['longitude']
                resd['device_country'] = location['country_name']
                resd['device_province'] = 'None'
                resd['device_city'] = location['city']
                res.append(resd)
        return res
if __name__ == '__main__':
    dp = DataPersistence()
    r = dp.get_data("D:/modbus.json")
    #print(r)
