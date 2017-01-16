import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='123456',
                             db='example_test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    # with connection.cursor() as cursor:
    #     # Create a new record
    #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #     cursor.execute(sql, ('sakeyoulai@111.s', '123'))
    #
    # # connection is not autocommit by default. So you must commit to save your changes.
    # connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users`"
        cursor.execute(sql)
        # result = cursor.fetchone()
        #
        print(cursor.fetchall())
        # print(result)
        print(cursor.description)
        for row in cursor:
            print(row)
        cursor.close()
finally:
    connection.close()