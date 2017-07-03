import pymysql, datetime, random
class ToVul:
    def __init__(self):
        self.conn = pymysql.connect(host='192.168.205.38',
                                    port=3306,
                                    user='root',
                                    password='123456',
                                    db='sol_daily',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    def to_vul(self):
        try:
            with self.conn.cursor() as cur:
                q_sql = "SELECT id, system_province, system_city, create_time,"\
                        "update_time, system_name FROM `stat_system_city` WHERE `system_country`='中国'"
                cur.execute(q_sql)
                objs = cur.fetchall()
                for i in objs:
                    flag = random.choice([True,False,True])
                    vul_desc = i['system_province']+"省"+i['system_city']+i['system_name']+"系统"
                    url1 = "./image/safetyStatistics/loopholes-1.png"
                    url2 = "./image/safetyStatistics/loopholes-2.png"
                    a = random.choice([0,0,0,0,0,1,1,1,1,2,2,2,3,3,3,4])
                    b = random.choice([0,0,0,0,1,1,1,2,2,3])
                    c = random.choice([0,0,0,0,0,0,0,1,1,2])
                    d = random.choice([0,0,1,1,1,2])
                    if flag:
                        i_sql = "INSERT INTO `stat_industrial_vul` (`vul_desc`, `vul_image_url`, `vul_date`, " \
                                "`create_time`, `update_time`, `system_id`, `vul_weak_pass`, `vul_logic`," \
                                " `vul_sql_inj`, `vul_code_exec`) " \
                                "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
                                %(vul_desc+"有漏洞",url1,i['create_time'],i['update_time'],self.now,i['id'],a,b,c,d)
                    else:
                        i_sql = "INSERT INTO `stat_industrial_vul` (`vul_desc`, `vul_image_url`, `vul_date`, " \
                                "`create_time`, `update_time`, `system_id`, `vul_weak_pass`, `vul_logic`," \
                                " `vul_sql_inj`, `vul_code_exec`) " \
                                "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
                                %(vul_desc+"暂无漏洞",url2,i['create_time'],i['update_time'],self.now,i['id'],0,0,0,0)
                    cur.execute(i_sql)
                    self.conn.commit()
        finally:
            self.conn.close()
if __name__ == '__main__':
    # sys = ToVul()
    # sys.to_vul()
    sql = "SELECT * FROM stat_industrial_vul WHERE system_id IN ("
    for i in range(1000):
        sql+=(str(i)+",")
    sql += ("1001)")
    print(sql)