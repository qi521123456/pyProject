import pymysql
import re
del_str = ["","None"]
alter_str = [{"siemens%":"Siemens"},{"v%"}]

q_sql = 'select * from sol_daily.device_all where vendor like "%US%"'
conn = pymysql.connect(host='10.0.10.10',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='sol_daily',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
with conn.cursor() as cur:
    cur.execute(q_sql)
    objlist = cur.fetchall()
    for obj in objlist:
        v = obj["vendor"]
        alt_vendor = re.sub(r',US',"",v,re.I)
        update_sql = "UPDATE device_all SET vendor='%s' WHERE id='%s'"%(alt_vendor,obj['id'])
        print(alt_vendor)
        # cur.execute(update_sql)
        # conn.commit()
conn.close()