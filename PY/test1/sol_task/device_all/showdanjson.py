import json
import datetime
import pymysql
import socket,struct
import sys
filename = "D:/cns7.json"
def get_data(filename=filename):
    res = []
    with open(filename,'r') as fr:
        #data = json.loads(json.dumps(fr.read()))
        data = eval(fr.read())
        for d in data['matches']:
            resd = {}
            info = d['data'].replace('\n', ':').split(':')
            if len(info) < 20:
                continue
            t = data['matches'][1]['timestamp']
            timestamp = t[:t.find('.')].replace('T',' ')
            ip = d['ip_str']
            port = d['port']
            location = d['location']
            i = 0
            dinfo = {}
            while i < 20:
                dinfo[info[i]] = info[i+1]
                i += 2
            cr = dinfo['Copyright']
            serial = dinfo['Serial number of module']
            module = dinfo['Module']
            module_type = dinfo['Module type']
            sys_name = dinfo['PLC name']
            try:
                version = dinfo['Basic Firmware']
                hardware = dinfo['Basic Hardware']
            except KeyError:
                version = 'None'
                hardware = 'None'
            resd['device_ip'] = ip
            resd['device_port'] = port
            resd['create_time'] = timestamp
            resd['basic_hardware'] = hardware
            resd['system_name'] = sys_name
            resd['module_type'] = module_type
            resd['module'] = module
            resd['version'] = version
            resd['serial_number'] = serial
            resd['copyright'] = cr
            resd['latitude'] = location['latitude']
            resd['longitude'] = location['longitude']
            resd['device_country'] = location['country_name']
            resd['device_province'] = 'None'
            resd['device_city'] = location['city']
            res.append(resd)
    return res
def _mysql_connect():
    connection = pymysql.connect(host='10.0.1.199',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='sol_daily',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
def to_s7comm(data):
    con = _mysql_connect()
    try:
        with con.cursor() as cursor:
            count = 0
            for d in data:
                ip = d['device_ip']
                q_sql = "SELECT device_ip FROM result_s7comm WHERE device_ip = '" + ip + "'"
                cursor.execute(q_sql)
                if len(cursor.fetchall()) != 0:
                    continue
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
                for k,v in d.items():
                    s1.append("`"+str(k)+"`")
                    s2.append("'"+str(v)+"'")
                insert_sql = "INSERT INTO result_s7comm (%s) VALUES (%s)" % (','.join(s1),','.join(s2))
                #print(insert_sql)
                cursor.execute(insert_sql)
                con.commit()
                count += 1
                # sys.stdout.write('\r%s%%' % str(round(count * 100 / len(data), 2)))
                # sys.stdout.flush()
    finally:
        con.close()



d = get_data()
to_s7comm(d)
#print('`.`'.join(["21q","2"]))
