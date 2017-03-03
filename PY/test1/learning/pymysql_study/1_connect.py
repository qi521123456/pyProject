import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='10.0.1.188',
                             port=3306,
                             user='root',
                             password='123456',
                             db='sol_daily',
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
        iplong = '2102229736'
        sql = "SELECT country, province, city FROM ip_ipipnet where ip_from < "+iplong+" and ip_to > "+iplong+""
        cursor.execute(sql)
        # result = cursor.fetchone()
        #
        print(cursor.fetchall()[0])
        # print(result)
        print(cursor.description)
        # for row in cursor:
        #     print(row)
        # cursor.close()
finally:
    connection.close()