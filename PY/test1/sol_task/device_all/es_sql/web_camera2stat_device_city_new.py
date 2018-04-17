

import json,datetime,pymysql
now = datetime.datetime.now()

a = json.load(open('D:/read.txt',encoding='utf8'))
china_data = a['aggregations']['product']['buckets']
conn = pymysql.connect(host='192.168.120.188',
                                 port=3306,
                                 user='sol',
                                 password='SolWi11',
                                 db='sol_daily',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()
for product_data in china_data:
    product_name = product_data['key']
    # if str(product_name).find('hikvision')!=-1:
    #     product_name = 'Hikvision'
    # elif str(product_name).lower().find('dahua')!=-1:
    #     product_name = 'Dahua'
    # elif str(product_name).lower().find('cisco')!=-1:
    #     product_name = 'Cisco'
    # elif str(product_name).lower().find('d-link')!=-1:
    #     product_name = 'd-link'
    # elif str(product_name).lower().find('tiandy')!=-1:
    #     product_name = 'Tiandy'
    # elif str(product_name).lower().find('tp')!=-1:
    #     product_name = 'tp-linkmaxtp-link'
    # elif str(product_name).lower().find('uniview')!=-1:
    #     product_name = 'uniview'
    if str(product_name).lower().find('xm')!=-1:
        product_name = 'XM'
    elif product_name.lower().find('uc_http')!=-1:
        product_name = 'Tiandy'
    else:
        print("--")
        continue
    for province_data in product_data['province']['buckets']:
        province_name = province_data['key']
        for city_data in province_data['city']['buckets']:
            city_name = city_data['key']
            num = city_data['doc_count']
            print("CN-%s-%s-%s-%s"%(province_name,city_name,product_name,num))
            insert_sql = "INSERT INTO stat_device_city_video_new (device_country, device_province, device_city, device_count, " \
                         "create_time, update_time, vendor) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % \
                                     ("中国",province_name,city_name,num,now,now,product_name)
            cur.execute(insert_sql)
            conn.commit()

print(now)