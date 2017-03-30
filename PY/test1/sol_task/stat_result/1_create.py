# coding=utf-8
import pymysql
import datetime
TABLES = ['result_iec104', 'result_melsec_q_tcp', 'result_melsec_q_udp', 'result_modbus', 'result_moxa',
          'result_s7comm', 'result_snmp', 'result_http', 'result_fox', 'result_fins', 'result_ethernetip',
          'result_bacnet', 'result_cspv4', 'result_dahua', 'result_dnp3']
VENDORS = [{'table_name': 'result_iec104', 'vendor': 'Unknown'},
           {'table_name': 'result_melsec_q_tcp', 'vendor': 'Mitsubishi'},
           {'table_name': 'result_melsec_q_udp', 'vendor': 'Mitsubishi'},
           {'table_name': 'result_modbus', 'vendor_name': 'vendor'},
           {'table_name': 'result_moxa', 'vendor_name': 'vendor'},
           {'table_name': 'result_s7comm', 'vendor_name': 'vendor'},
           {'table_name': 'result_snmp', 'vendor_name': 'vendor'},
           {'table_name': 'result_http', 'vendor_name': 'device'},
           {'table_name': 'result_fox', 'vendor_name': 'brand_id'},
           {'table_name': 'result_fins', 'vendor': 'Omron'},
           {'table_name': 'result_ethernetip', 'vendor_name': 'vendor'},
           {'table_name': 'result_bacnet', 'vendor_name': 'vendor_name'},
           {'table_name': 'result_cspv4', 'vendor': 'Unknown'},
           {'table_name': 'result_dahua', 'vendor_name': 'device'},
           {'table_name': 'result_dnp3', 'vendor': 'Unknown'}
           ]
class DataCollection:
    def __init__(self,host="10.0.1.199"):
        self.host = host
        self.tables = TABLES
        self.now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    def __mysql_connect(self):
        connection = pymysql.connect(host=self.host,
                                     port=3306,
                                     user='root',
                                     password='123456',
                                     db='sol_daily',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    def stat_device_all(self):
        con = self.__mysql_connect()
        tables = self.tables
        vendors = VENDORS
        brand_count = 0
        device_count = 0
        province_count = 0
        vendor_count = 0
        try:
            with con.cursor() as cursor:
                brand = {}
                vendor_sql = "select count(id) as count from `stat_device_vendor`"
                cursor.execute(vendor_sql)
                vendor_count = cursor.fetchone()['count']
                for tablename in tables:
                    t = "select * from %s limit 1" % tablename
                    cursor.execute(t)
                    d = cursor.fetchone()
                    for i,v in d.items():
                        if i.find('brand') != -1:
                            brand[tablename] = i
                    device_sql = "select count(id) as count from (select id,device_ip from %s group by device_ip) as " \
                                 "t" % tablename
                    cursor.execute(device_sql)
                    device_count += cursor.fetchone()['count']
                    province_sql = "select count(id) as count from (select id,device_province from %s where " \
                                   "device_country='中国' group by device_province) as t" % tablename
                    cursor.execute(province_sql)
                    province_count += cursor.fetchone()['count']
                for table in tables:  # brand_count如果没有类似brand的列则按照VENDORS里的若1.vendor则+1,若2.vendor_name则+对应列的不同商标数目
                    if table in brand:
                        brand_sql = "SELECT count(id) as brand_count FROM (SELECT id,{1} from {0} " \
                                    "group by {1}) as t".format(table,brand[table])
                        cursor.execute(brand_sql)
                        brand_count += cursor.fetchone()['brand_count']
                    else:
                        for vendor in vendors:
                            if vendor['table_name'] == table:
                                if 'vendor' in vendor:
                                    if vendor['vendor'] != 'Unknown':
                                        brand_count += 1
                                    else:
                                        break
                                else:
                                    brand_sql = "SELECT count(id) as brand_count FROM (SELECT id,{1} from {0} " \
                                                "group by {1}) as t".format(table,vendor['vendor_name'])
                                    cursor.execute(brand_sql)
                                    brand_count += cursor.fetchone()['brand_count']
                                break
                print(vendor_count,brand_count,province_count,device_count)
                update_sql = "UPDATE stat_device_all SET device_count = '%s',update_time = '%s',province_count" \
                             " = '%s',brand_count = '%s',vendor_count = '%s' WHERE id = 1" \
                             "" % (device_count, self.now,province_count,brand_count,vendor_count)
                cursor.execute(update_sql)
                con.commit()
        finally:
            con.close()
    def stat_device_city(self):
        con = self.__mysql_connect()
        citys = {}
        try:
            with con.cursor() as cursor:
                for tablename in self.tables:
                    q_sql = "SELECT device_country,device_province,device_city,count(device_ip) as device_count from " \
                            "(select * from %s group by device_ip) as t " \
                            "group by device_country,device_province,device_city" % tablename
                    cursor.execute(q_sql)
                    info = cursor.fetchall()
                    for i in info:
                        k = '@'.join([i['device_country'],i['device_province'],i['device_city']])
                        v = i['device_count']
                        if k not in citys:
                            citys[k] = v
                        else:
                            citys[k] += v
                for city,count in citys.items():
                    s = city.split('@')
                    isin_sql = "SELECT id FROM stat_device_city where device_country = '%s' and device_province = '%s' " \
                               "and device_city = '%s'" % (s[0],s[1],s[2])
                    update_sql = "UPDATE stat_device_city SET device_count = '%s',update_time = '%s' WHERE " \
                                 "device_country = '%s' and device_province = '%s' and device_city = '%s'" \
                                 "" % (count,self.now,s[0],s[1],s[2])
                    insert_sql = "INSERT INTO stat_device_city (`device_country`,`device_province`,`device_city`," \
                                 "`device_count`,`create_time`,`update_time`) VALUES " \
                                 "('%s','%s','%s','%s','%s','%s')" % (s[0],s[1],s[2],count,self.now,self.now)
                    cursor.execute(isin_sql)
                    if cursor.fetchone() is None:
                        cursor.execute(insert_sql)
                    else:
                        cursor.execute(update_sql)
                    con.commit()
        finally:
            con.close()

    def stat_device_protocol(self):
        con = self.__mysql_connect()
        try:
            with con.cursor() as cursor:
                ids = {}
                for tablename in self.tables:
                    q_sql = "SELECT count(id) as count,device_port FROM (select id,device_port from %s group by " \
                            "device_ip) as t" % tablename
                    cursor.execute(q_sql)
                    d = cursor.fetchone()
                    qpid_sql = "SELECT id FROM protocol WHERE protocol_port = '%s'" % d['device_port']
                    cursor.execute(qpid_sql)
                    protocol_id = cursor.fetchone()['id']
                    ids[protocol_id] = d['count']
                for i,count in ids.items():
                    isin_sql = "SELECT id FROM stat_device_protocol where protocol_id = '%s'" % i
                    update_sql = "UPDATE stat_device_protocol SET protocol_id = '%s',update_time = '%s',device_count" \
                                 " = '%s' WHERE protocol_id = '%s'" \
                                 "" % (i, self.now, count, i)
                    insert_sql = "INSERT INTO stat_device_protocol (`protocol_id`,`device_count`,`update_time`," \
                                 "`create_time`) VALUES " \
                                 "('%s','%s','%s','%s')" % (i,count,self.now,self.now)
                    cursor.execute(isin_sql)
                    if cursor.fetchone() is None:
                        cursor.execute(insert_sql)
                    else:
                        cursor.execute(update_sql)
                    con.commit()
        finally:
            con.close()
    def stat_device_vendor(self):
        con = self.__mysql_connect()
        vendors = VENDORS
        try:
            with con.cursor() as cursor:
                res = {}
                for vendor in vendors:
                    if not 'vendor' in vendor:
                        q_sql = "select {1} as vendor,count(id) as count from (select id,{1},device_ip from {0} " \
                                "group by device_ip) as t " \
                                "group by {1}".format(vendor['table_name'], vendor['vendor_name'])
                    elif vendor['vendor'] != 'Unknown':
                        q_sql = "select count(id) as count from (select id from {0} group by device_ip) as " \
                                "t".format(vendor['table_name'])
                    else:
                        continue
                    cursor.execute(q_sql)
                    d = cursor.fetchall()
                    if len(d[0]) == 1:
                        d[0]['vendor'] = vendor['vendor']
                    for i in d:
                        vendorname = str(i['vendor']).split(' ')[0].lower().capitalize()
                        count = i['count']
                        if vendorname == '' or vendorname == 'None':
                            continue
                        elif vendorname in res:
                            res[vendorname] += count
                        else:
                            res = self.__revise_res(vendorname,count,res)
                #print(res)
                for i,count in res.items():
                    isin_sql = "SELECT id FROM stat_device_vendor where vendor = '%s'" % i
                    update_sql = "UPDATE stat_device_vendor SET vendor = '%s',update_time = '%s',device_count" \
                                 " = '%s' WHERE vendor = '%s'" \
                                 "" % (i, self.now, count, i)
                    insert_sql = "INSERT INTO stat_device_vendor (`vendor`,`device_count`,`update_time`," \
                                 "`create_time`) VALUES " \
                                 "('%s','%s','%s','%s')" % (i,count,self.now,self.now)
                    cursor.execute(isin_sql)
                    if cursor.fetchone() is None:
                        cursor.execute(insert_sql)
                    else:
                        cursor.execute(update_sql)
                    con.commit()


        finally:
            con.close()
    def __revise_res(self,s,c,res):
        for k,v in res.items():
            if k.find(s) != -1:
                res[k] += c
                return res
            elif s.find(k) != -1:
                res[s] = c+v
                del res[k]
                return res
        res[s] = c
        return res

def main():
    dc = DataCollection()
    dc.stat_device_vendor()
    dc.stat_device_city()
    dc.stat_device_protocol()
    dc.stat_device_all()  # 一定要在stat_device_vendor后


if __name__ == '__main__':
    main()
