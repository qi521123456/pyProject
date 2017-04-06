# coding:utf-8
from docx import Document
from openpyxl import Workbook,load_workbook
from openpyxl.styles import Font,colors
import matplotlib.pyplot as plt
from pylab import mpl
import pymysql
import datetime,os
ICDTABLES = [{'table_name': 'result_iec104', 'vendor': '未知', 'device_info':None},
             {'table_name': 'result_melsec_q_tcp', 'vendor': 'Mitsubishi', 'device_info':'cpuinfo'},
             {'table_name': 'result_melsec_q_udp', 'vendor': 'Mitsubishi', 'device_info':'cpuinfo'},
             {'table_name': 'result_modbus', 'vendor_name': 'vendor', 'vendor': None, 'device_info':'device'},
             {'table_name': 'result_moxa', 'vendor_name': 'vendor', 'vendor': None, 'device_info':'server_name'},
             {'table_name': 'result_s7comm', 'vendor_name': 'vendor', 'vendor': None, 'device_info':'basic_hardware'},
             {'table_name': 'result_snmp', 'vendor_name': 'vendor', 'vendor': None, 'device_info':'cpu'},
             {'table_name': 'result_fox', 'vendor_name': 'brand_id', 'vendor': None, 'device_info':None},
             {'table_name': 'result_fins', 'vendor': 'Omron', 'device_info':'controller_model'},
             {'table_name': 'result_ethernetip', 'vendor_name': 'vendor', 'vendor': None, 'device_info':'product_name'},
             {'table_name': 'result_bacnet', 'vendor_name': 'vendor_name', 'vendor': None, 'device_info':'object_name'},
             {'table_name': 'result_cspv4', 'vendor': '未知', 'device_info':None},
             {'table_name': 'result_dnp3', 'vendor': '未知', 'device_info':None}
             ]
IofTABLES = ['result_http', 'result_dahua']
def get_data(province,month):  # province为汉字省份，month为二位数月份（01,02....12）
    con = pymysql.connect(host='10.0.1.199',
                          port=3306,
                          user='root',
                          password='123456',
                          db='sol_daily',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)
    year = datetime.datetime.now().strftime('%Y')
    icdTables = ICDTABLES
    iofTables = IofTABLES
    icdData = []
    iofData = []
    try:
        with con.cursor() as cursor:
            ipsicd = []
            for table in icdTables:
                table_name = table['table_name']
                vendor = table['vendor']
                info = table['device_info']
                if vendor is None and info is None:
                    q_sql = "SELECT device_ip,device_city,device_port,create_time,%s as vendor FROM %s " \
                            "WHERE device_province='%s'" % (table['vendor_name'],table_name,province)
                elif vendor is not None and info is None:
                    q_sql = "SELECT device_ip,device_city,device_port,create_time FROM %s " \
                            "WHERE device_province='%s'" % (table_name,province)
                elif vendor is None and info is not None:
                    q_sql = "SELECT device_ip,device_city,device_port,create_time,%s as vendor,%s as info FROM %s " \
                            "WHERE device_province='%s'" % (table['vendor_name'],info,table_name,province)
                else:
                    q_sql = "SELECT device_ip,device_city,device_port,create_time,%s as info FROM %s " \
                            "WHERE device_province='%s'" % (info,table_name,province)
                cursor.execute(q_sql)
                tmp = cursor.fetchall()
                if tmp is None:
                    continue
                for data in tmp:
                    d = {}
                    # print(str(year) + '-' + str(month),data['create_time'].strftime('%Y-%m'))
                    if data['create_time'].strftime('%Y-%m') != str(year) + '-' + str(month):
                        continue
                    d['ip'] = data['device_ip']
                    d['location'] = province + data['device_city']
                    d['port'] = data['device_port']
                    if vendor is None:
                        vendor = data['vendor']
                    d['vendor'] = vendor
                    d['info'] = "None"
                    if info is not None:
                        d['info'] = data['info']
                    p_sql = "SELECT protocol_name FROM protocol WHERE protocol_port='%s'" % d['port']
                    cursor.execute(p_sql)
                    protocol = cursor.fetchone()
                    if protocol is None:
                        proto = "未知"
                    else:
                        proto = protocol['protocol_name']
                    d['protocol'] = proto
                    if d['ip'] in ipsicd:
                        continue
                    ipsicd.append(d['ip'])
                    icdData.append(d)
            ipsiof = []
            for table in iofTables:
                q_sql = "SELECT create_time,device_ip,device_city,device_port,device FROM %s " \
                        "WHERE device_province='%s'" % (table,province)
                cursor.execute(q_sql)
                tmp = cursor.fetchall()
                if tmp is None:
                    continue
                for data in tmp:
                    d = {}
                    #print(str(year) + '-' + str(month),data['create_time'].strftime('%Y-%m'))
                    if data['create_time'].strftime('%Y-%m') != str(year)+'-'+str(month):
                        continue
                    d['ip'] = data['device_ip']
                    d['location'] = province+data['device_city']
                    d['port'] = data['device_port']
                    d['vendor'] = data['device']
                    p_sql = "SELECT protocol_name FROM protocol WHERE protocol_port='%s'" % d['port']
                    cursor.execute(p_sql)
                    protocol = cursor.fetchone()
                    if protocol is None:
                        proto = "未知"
                    else:
                        proto = protocol['protocol_name']
                    d['protocol'] = proto
                    if d['ip'] in ipsiof:
                        continue
                    ipsiof.append(d['ip'])
                    iofData.append(d)
    finally:
        con.close()
    return icdData,iofData
def draw_pie(info,province,path):
    location = {}
    vendor = {}
    protocol = {}
    tmp = {'location':location,'vendor':vendor,'protocol':protocol}
    for i in info:
        for k,v in tmp.items():
            if i[k] in v:
                v[i[k]] += 1
            else:
                v[i[k]] = 1
    for name,data in tmp.items():
        mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体 解决中文显示问题
        plt.figure()
        if name == 'location':
            title = province+"联网核心工控设备地区分布图"
        elif name == 'vendor':
            title = province+"联网核心工控设备厂商分布图"
        else:
            title = province+"联网核心工控设备协议分布图"
        plt.title(title)
        labels = []
        sizes = []
        for k,v in data.items():
            labels.append(k)
            sizes.append(v)
        #colors = ['red', 'yellowgreen', 'lightskyblue']
        plt.pie(sizes, labels=labels,autopct='%3.1f%%', shadow=False,startangle=90, pctdistance=0.8)
        plt.axis('equal')
        plt.legend(loc='upper right')
        # plt.show()
        plt.savefig(path+name+".png")
        plt.close()
def draw_grid(data,filename):
    # if os.path.exists(filename):
    #     wb = load_workbook(filename)
    # else:
    #     wb = Workbook(filename)
    name1 = "所有设备"
    name2 = "有信息设备"
    wb = Workbook(filename)
    ws = wb.create_sheet(name1)
    # ws = wb.active
    # ws = wb.create_sheet(name1)
    #ws.title = name1
    ft = Font(name='Courier New', size=12, color=colors.BLACK, bold=True)
    # wb.create_sheet(name1)
    # ws = wb.get_sheet_by_name(name1)

    ws.cell('A1').value = 'IP'
    ws['B1'].value = '协议'
    ws['C1'].value = '端口'
    ws['D1'].value = '位置'
    ws['E1'].value = '厂商'
    ws['A1'].font = ft
    ws['B1'].font = ft
    ws['C1'].font = ft
    ws['D1'].font = ft
    ws['E1'].font = ft
    for row,d in enumerate(data):
        #for col in range(0,5):
        ws.cell(column=0,row=row+1,value=d['ip'])
        ws.cell(column=1, row=row + 1, value=d['protocol'])
        ws.cell(column=2, row=row + 1, value=d['port'])
        ws.cell(column=3, row=row + 1, value=d['location'])
        ws.cell(column=4, row=row + 1, value=d['vendor'])
    if 'info' in data[0]:
        infos = []
        for i in data:
            if (i['info'] == 'None') or (i['info'].strip() == '') or (i['info'] == 'xxxxxx'):
                continue
            infos.append(i)
        ws2 = wb.create_sheet(name2)
        ws2['A1'].value = 'IP'
        ws2['B1'].value = '协议'
        ws2['C1'].value = '位置'
        ws2['D1'].value = '厂商'
        ws2['E1'].value = '设备信息'
        ws2['A1'].font = ft
        ws2['B1'].font = ft
        ws2['C1'].font = ft
        ws2['D1'].font = ft
        ws2['E1'].font = ft
        for row, d in enumerate(infos):
            ws2.cell(column=0, row=row + 1, value=d['ip'])
            ws2.cell(column=1, row=row + 1, value=d['location'])
            ws2.cell(column=2, row=row + 1, value=d['vendor'])
            ws2.cell(column=3, row=row + 1, value=d['protocol'])
            ws2.cell(column=4, row=row + 1, value=d['info'])
    wb.save(filename)



if __name__ == '__main__':
    a,b = get_data('河北','03')
    print(a,'\n',b)
    draw_grid(a,"D:/test.xlsx")
    #draw_pie(b,'HEIBEI','D:/')
