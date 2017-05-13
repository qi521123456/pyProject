import requests
import pymysql.cursors
def get_ips():
    connection = pymysql.connect(host='10.0.1.188',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='sol',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "SELECT device_ip FROM result_http WHERE device = 'XM'"
        cursor.execute(sql)
        #print(cursor.fetchall())
        ips = []
        for row in cursor:
            ips.append(row['device_ip'])
        cursor.close()
    connection.close()
    return ips

print(get_ips())
login_page_ips = []
for ip in get_ips():
    try:
        r = requests.get("http://" + ip, timeout=1)
        if r.status_code == 200:
            login_page_ips.append(ip)
    except:
        pass
print(login_page_ips)