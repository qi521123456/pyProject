import pymysql.cursors


class MysqlInterface:

    def __init__(self,host,user,password,db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = "utf8mb4"
        self.cursor = pymysql.cursors.DictCursor
        self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db,
                                     charset=self.charset, cursorclass=self.cursor)

    def insert(self, sql):
        try:
            connection = self.connection
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()
        except Exception as e:
            print(e)

    def query(self, sql):
        try:
            connection = self.connection
            with connection.cursor() as cursor:
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except Exception as e:
            print(e)