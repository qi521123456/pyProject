
import pymysql.cursors


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
	conn = MysqlInterface(host="10.0.1.188", user="root", password="123456", db="sol_daily")
	# sql = "INSERT INTO `bookbase`(`bookId`, `bookName`) VALUES ('13', 'ThirdBooka')"
	# conn.insert(sql)
	q_sql = 'select device_ip from fofa'
	res = conn.query(q_sql)
	# print(conn.query(q_sql))
	with open('D:/ips.txt','w') as f:
		for row in res:
			f.writelines(row['device_ip']+'\n')


