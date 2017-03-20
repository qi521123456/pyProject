import pymysql
import datetime
import sys
class Migration():
    tableinfo = [{'table_name': 'iec104', 'vendor': 'Unknown'},
                 {'table_name': 'melsec_q_tcp', 'vendor': 'Mitsubishi'},
                 {'table_name': 'melsec_q_udp', 'vendor': 'Mitsubishi'},
                 {'table_name': 'modbus', 'vendor_name': 'vendor'},
                 {'table_name': 'moxa', 'vendor_name': 'vendor'},
                 {'table_name': 's7comm', 'vendor_name': 'vendor'},
                 {'table_name': 'snmp', 'vendor_name': 'vendor'},
                 {'table_name': 'http', 'vendor_name': 'device'},
                 {'table_name': 'fox', 'vendor_name': 'brand_id'},
                 {'table_name': 'fins', 'vendor': 'Omron'},
                 {'table_name': 'ethernetip', 'vendor_name': 'vendor'},
                 {'table_name': 'bacnet', 'vendor_name': 'vendor_name'},
                 {'table_name': 'cspv4', 'vendor': 'Unknown'},
                 {'table_name': 'dahua', 'vendor_name': 'device'},
                 {'table_name': 'dnp3', 'vendor': 'Unknown'}
                 ]
    def __init__(self):

        self.conn = pymysql.connect(host='10.0.1.188',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='sol_daily',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        self.now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.tablenames = [name['table_name'] for name in self.tableinfo]


    def __get_result(self,tables):
        reslist = list()
        for table in tables:
            vender = None
            if table not in self.tablenames:
                continue
            for info in self.tableinfo:
                if info['table_name'] is table:
                    if info.get('vendor') is None:
                        vendorname = info.get('vendor_name')
                        q_sql = "SELECT create_time,device_ip,device_port,device_country,device_province,device_city,%s " \
                                "FROM result_%s" % (vendorname,table)
                    else:
                        vender = info.get('vendor')
                        q_sql = "SELECT create_time,device_ip,device_port,device_country,device_province,device_city " \
                                "FROM result_%s" % table

            try:
                with self.conn.cursor() as cursor:
                    # q_sql = "SELECT create_time,device_ip,device_port,device_country,device_province,device_city,device " \
                    #         "FROM result_cspv4"
                    cursor.execute(q_sql)
                    objlist = cursor.fetchall()
                    for obj in objlist:
                        res = dict()
                        res['protocol'] = "*"
                        res['ip'] = obj['device_ip']
                        res['port'] = obj['device_port']
                        res['create_time'] = obj['create_time']
                        res['country'] = obj['device_country']
                        res['province'] = obj['device_province']
                        res['city'] = obj['device_city']
                        if vender is None:
                            res['vendor'] = obj.get(vendorname)
                        else:
                            res['vendor'] = vender
                        query_protocol_sql = "SELECT protocol_name FROM protocol WHERE protocol_port='%s'" % obj[
                            'device_port']
                        cursor.execute(query_protocol_sql)
                        protoc = cursor.fetchone()
                        if protoc is not None:
                            res['protocol'] = protoc['protocol_name']
                        reslist.append(res)
            except:
                pass
        print("begin write")
        return reslist

    def to_deviceall(self,reslist):
        #reslist = list()
        try:
            with self.conn.cursor() as cursor:
                for res in reslist:
                    ip = res['ip']
                    port = res['port']
                    country = res['country']
                    province = res['province']
                    city = res['city']
                    protocol = res['protocol']
                    vendor = res['vendor']
                    first_time = res['create_time']
                    last_time = res['create_time']
                    create_time = self.now
                    update_time = self.now

                    query_sql = "SELECT id,first_time,last_time FROM device_all WHERE device_ip='%s'" % ip
                    update_sql = None
                    cursor.execute(query_sql)
                    exist_ip = cursor.fetchone()
                    if exist_ip is not None:
                        if exist_ip['first_time'].strftime('%Y-%m-%d %H:%M:%S') > first_time.strftime('%Y-%m-%d %H:%M:%S'):
                            update_sql = "UPDATE device_all SET `first_time`='%s',`update_time`='%s' WHERE id=%s" % (first_time,update_time,exist_ip['id'])
                        elif exist_ip['last_time'].strftime('%Y-%m-%d %H:%M:%S') < last_time.strftime('%Y-%m-%d %H:%M:%S'):
                            update_sql = "UPDATE device_all SET `last_time`='%s',`update_time`='%s' WHERE id=%s" % (last_time,update_time,exist_ip['id'])
                    else:
                        insert_sql = "INSERT INTO device_all (`device_ip`, `device_port`, `device_country`, " \
                                     "`device_province`, `device_city`, `protocol`, `vendor`, `first_time`, `last_time`, " \
                                     "`create_time`, `update_time`) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'" \
                                     ",'%s')" % \
                                     (ip,port,country,province,city,protocol,vendor,first_time,last_time,create_time,update_time)
                    if update_sql is None:
                        cursor.execute(insert_sql)
                        self.conn.commit()
                    else:
                        cursor.execute(update_sql)
                        self.conn.commit()
                    sys.stdout.write('\r%s%%' % str(round(reslist.index(res) * 100 / (len(reslist)-1), 2)))
                    sys.stdout.flush()
        finally:
            self.conn.close()

    def begin(self):
        self.to_deviceall(self.__get_result(self.tablenames))


def main():
    m = Migration()
    m.begin()



if __name__ == '__main__':
    main()

