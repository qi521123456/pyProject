
import pymysql.cursors
import datetime

class MysqlInterface:
	def __init__(self, host, user, password, db):
		self.host = host
		self.user = user
		self.password = password
		self.db = db
		self.charset = "utf8mb4"
		self.cursorclass = pymysql.cursors.DictCursor

	def connect(self):
		connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db,
									charset=self.charset, cursorclass=self.cursorclass)
		return connection

	def insert(self, sql):
		try:
			connection = self.connect()
			with connection.cursor() as cursor:
				cursor.execute(sql)
			connection.commit()
		except Exception as e:
			print(e)

	def query(self, sql):
		try:
			connection = self.connect()
			with connection.cursor() as cursor:
				cursor.execute(sql)
				res = cursor.fetchall()
				return res
		except Exception as e:
			print(e)

if __name__ == '__main__':
	now = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
	conn = MysqlInterface(host="192.168.205.38", user="root", password="123456", db="sol_daily")
	sql1 = "INSERT INTO `stat_system_city`(`system_country`, `system_province`,`system_city`,`system_ip`,`system_id`," \
		  "`create_time`,`update_time`) VALUES ('中国', '河北', '石家庄','192.168.0.1','2','%s','%s')"%(now,now)

	for i in range(1,50):
		sql2 = "INSERT INTO stat_industrial_vul (vul_desc, vul_image_url, val_date, create_time, update_time) VALUES ('漏洞：%s','/home/image/%s.jpg','%s','%s','%s')" \
			   ""%(str(i),str(i),now,now,now)
		print(sql2)
		conn.insert(sql2)
	# q_sql = 'select device_ip from fofa'
	# res = conn.query(q_sql)
	# print(conn.query(q_sql))
	# with open('D:/ips.txt','w') as f:
	# 	for row in res:
	# 		f.writelines(row['device_ip']+'\n')


