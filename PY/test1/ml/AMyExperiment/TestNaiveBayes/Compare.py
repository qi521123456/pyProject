import time
import pymysql
conn = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='duduDemo',
                                 charset='utf8mb4')
now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()-24*60*60*30))
print(now,type(now))
cur = conn.cursor()
s_sql = "select update_time from main_domain limit 1"
snum = cur.execute(s_sql)

updatetime = cur.fetchone()[0]
print(snum,updatetime)
print(now>str(updatetime))
