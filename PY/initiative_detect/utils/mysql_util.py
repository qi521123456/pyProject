"""
@version: ??
@author: lihongbiao
@file: mysql_util.py.py
@time: 2016/12/9 10:35
"""
import pymysql.cursors

# connect to database
connection = pymysql.connect(host="localhost", user="root", password="123456", db="test",
                             charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
try:
	with connection.cursor() as cursor:
		sql = "INSERT INTO `bookbase`(`bookId`, `bookName`) VALUES (%s, %s)"
		cursor.execute(sql, ("10", "myBook"))
	connection.commit()

	with connection.cursor() as cursor:
		sql = "SELECT * FROM `bookbase` WHERE bookId=%s"
		cursor.execute(sql, ("10",))
		result = cursor.fetchone()
		print(result)
finally:
	connection.close()