# coding=utf-8

import sys

# reload(sys)
# sys.setdefaultencoding('utf8')

import pymysql
import pymongo
import datetime
from bson.objectid import ObjectId
TABLES = ['result_iec104', 'result_melsec_q_tcp', 'result_melsec_q_udp', 'result_modbus', 'result_moxa',
          'result_s7comm', 'result_snmp', 'result_http', 'result_fox', 'result_fins', 'result_ethernetip',
          'result_bacnet', 'result_cspv4', 'result_dahua', 'result_dnp3']
INFOS = [{'table_name': 'result_iec104', 'vendor': 'Unknown', 'device_info':None},
         {'table_name': 'result_melsec_q_tcp', 'vendor': 'Mitsubishi', 'device_info':'cpuinfo'},
         {'table_name': 'result_melsec_q_udp', 'vendor': 'Mitsubishi', 'device_info':'cpuinfo'},
         {'table_name': 'result_modbus', 'vendor_name': 'vendor', 'vendor': None, 'device_info':'device'},
         {'table_name': 'result_moxa', 'vendor_name': 'vendor', 'vendor': None, 'device_info':'server_name'},
         {'table_name': 'result_s7comm', 'vendor_name': 'vendor', 'vendor': None, 'device_info':'basic_hardware'},
         {'table_name': 'result_snmp', 'vendor_name': 'vendor', 'vendor': None, 'device_info':'cpu'},
         {'table_name': 'result_fox', 'vendor_name': 'brand_id', 'vendor': None, 'device_info':None},
         {'table_name': 'result_fins', 'vendor': 'Omron', 'device_info':'controller_model'},
         {'table_name': 'result_ethernetip', 'vendor_name': 'vendor', 'vendor': None, 'device_info':'product_name'},
         {'table_name': 'result_bacnet', 'vendor_name': 'vendor_name', 'vendor': None, 'device_info':'object_name'},
         {'table_name': 'result_cspv4', 'vendor': 'Unknown', 'device_info':None},
         {'table_name': 'result_dnp3', 'vendor': 'Unknown', 'device_info':None},
         {'table_name': 'result_http', 'vendor': None, 'vendor_name': 'device','device_info':None},
         {'table_name': 'result_dahua', 'vendor': None, 'vendor_name': 'device','device_info':None}
         ]
if __name__ == '__main__':
    tables = TABLES
    infos = INFOS
    mysql_connection = pymysql.connect(host='10.0.1.199', user='root', passwd='123456', db='sol_daily', port=3306,
                                       charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
    #sql = 'select * from content_cert'
    #mysql_cursor = mysql_connection.cursor()
    results = []
    try:
        with mysql_connection.cursor() as mysql_cursor:
            ip_time = {}
            for table in infos:
                table_name = table['table_name']
                vendor = table['vendor']
                info = table['device_info']
                if vendor is None and info is None:
                    q_sql = "SELECT device_ip,device_country,device_province,device_city,device_port,create_time," \
                            "%s as vendor FROM %s " % (table['vendor_name'], table_name)
                elif vendor is not None and info is None:
                    q_sql = "SELECT device_ip,device_country,device_province,device_city,device_port,create_time FROM %s " \
                            "" % table_name
                elif vendor is None and info is not None:
                    q_sql = "SELECT device_ip,device_country,device_province,device_city,device_port," \
                            "create_time,%s as vendor,%s as info FROM %s " % (table['vendor_name'], info, table_name)
                else:
                    q_sql = "SELECT device_ip,device_country,device_province,device_city,device_port,create_time," \
                            "%s as info FROM %s " % (info, table_name)
                mysql_cursor.execute(q_sql)
                tmp = mysql_cursor.fetchall()
                if tmp is None:
                    continue
                for data in tmp:
                    d = {}
                    d['ip'] = data['device_ip']
                    d['country'] = data['device_country']
                    d['province'] = data['device_province']
                    d['city'] = data['device_city']
                    d['port'] = data['device_port']
                    if vendor is None:
                        vendor = data['vendor']
                    d['vendor'] = vendor
                    if info is not None:
                        d['fingerprint'] = data['info']
                    else:
                        d['fingerprint'] = ""
                    p_sql = "SELECT protocol_name,port_type FROM protocol WHERE protocol_port='%s'" % d['port']
                    mysql_cursor.execute(p_sql)
                    protocol = mysql_cursor.fetchone()
                    if protocol is None:
                        proto = ""
                        pt = ""
                    else:
                        proto = protocol['protocol_name']
                        pt = protocol['port_type']
                    d['protocol_application'] = proto
                    d['protocol_transport'] = pt
                    d['update_time'] = data['create_time']
                    d['location'] = ""
                    d['product'] = ""
                    d['op_type'] = "a"
                    if d['ip'] in ip_time:  # 去重
                        if ip_time[d['ip']] >= d['update_time']:
                            continue
                    ip_time[d['ip']] = d['update_time']
                    results.append(d)

    # except Exception as e:
    #     print(Exception, ":", e)
    finally:
        mysql_connection.close()
    #print(results)
    # 写入Mongo
    mongo_client = pymongo.MongoClient("mongodb://anydb_admin:xinliankehui@10.0.20.33:27017/admin")
    mongo_db = mongo_client["Norn2"]
    mongo_collection = mongo_db.ResultProbe

    mongo_collection.insert(results)

    # test_find_one = table_name.find_one({"status":"test"})
    # test_find = table_name.find({"status":"test"})