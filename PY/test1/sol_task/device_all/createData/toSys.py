import pymysql, datetime, sys,random
class ToSysCity:
    def __init__(self):
        self.conn = pymysql.connect(host='192.168.205.38',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='sol_daily',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        self.now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    def to_sys(self):
        try:
            with self.conn.cursor() as cur:
                q_sql = "SELECT device_ip, device_port, device_country, device_province, device_city, first_time," \
                        " vendor,protocol,id FROM device_all"
                cur.execute(q_sql)
                objs = cur.fetchall()
                for i in objs:
                    x = random.randint(1, 7)
                    name = i['vendor']+i['protocol']+str(i['id'])
                    if x<4:
                        sys_type = "Electricity"
                    elif x<6:
                        sys_type = "Gas"
                    elif x<7:
                        sys_type = "Water"
                    else:
                        sys_type = "Coal"
                    i_sql = "INSERT INTO `stat_system_city` (`system_country`, `system_province`, `system_city`, " \
                            "`system_ip`, `system_port`, `create_time`, `update_time`, `system_name`, `system_type`) " \
                            "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
                            % (i['device_country'],i['device_province'],i['device_city'],i['device_ip'],
                               i['device_port'],i['first_time'],self.now,name,sys_type)
                    cur.execute(i_sql)
                    self.conn.commit()
        finally:
            self.conn.close()

if __name__ == '__main__':
    toSys = ToSysCity()
    toSys.to_sys()