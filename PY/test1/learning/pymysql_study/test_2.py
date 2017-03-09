import pymysql

connection = pymysql.connect(host='10.0.1.188',
                             port=3306,
                             user='root',
                             password='123456',
                             db='sol_daily',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
ips = []
try:
    with connection.cursor() as cursor:
        ip = '77.242.22.193'
        sql = "SELECT device_ip FROM result_s7comm WHERE version = 'None'"
        q_sql = "SELECT device_ip FROM fofa WHERE device_ip = '"+ip+"'"
        cursor.execute(q_sql)
        print(len(cursor.fetchall()) == 0)
       #with open('D:/ip.txt','w') as opener:
        # for ip in cursor:
        #     #print(ip)
        #     ips.append(ip.get('device_ip'))
        cursor.close()
finally:
    connection.close()

# print(len(list(set(ips))))

# with open('D:/ip.txt','w') as opener:
#     for row in list(set(ips)):
#         opener.write(row)
#         opener.write('\n')