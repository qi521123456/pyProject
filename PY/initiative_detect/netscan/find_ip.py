try:
    import sys
    import math
    from ipaddress import ip_address, ip_network
    from utils.mongodb import MongoDBInterface
except Exception as e:
    print(e)

def math_ip_list(start_ip,end_ip):
    try:
        ip0 = ip_address(start_ip)
        ip1 = ip_address(end_ip)
        count = int(ip1)-int(ip0)+1
        length_base2 = math.log(count, 2)
        ip_list = []
        if int(length_base2) != length_base2:
            temp = 0
            while temp < count:
                ip_list.append(str(ip0 + temp))
                temp += 1
        else:
            data = u'%s/%d' % (str(ip0), 32-int(length_base2))
            #network = ip_network(data)
            ip_list.append(data)
        return ip_list
    except Exception as e:
        return e

def find_location(ip):
    try:
        handler = mongodb.MongoDBInterface()
        handler.connect('127.0.0.1','SOL','admin','Free-Wi11')
        res_list = handler.query(None, "IPSearch", {})
        for res in res_list:
            start_ip = ip_address(res.get('start_ip'))
            end_ip = ip_address(res.get('end_ip'))
            ip = ip_address(ip)
            if ip >= start_ip and ip <= end_ip:
                return res.get('location')
    except Exception as e:
        return e

# if __name__ == '__main__':
    # ip_list = math_ip_list('36.110.36.27','36.110.147.122')
    # for each in ip_list:
    #     print(each)
    # print(find_location('36.110.146.27'))


if __name__ == '__main__':
    mi = MongoDBInterface()
    mi.connect('localhost','SOL','root','Free-Wi11')
    res = mi.query(None,'ChinaIP',{'province':'浙江'})
    ips = res[0].get('ips')
    file = open('zj.txt','w+',encoding='UTF-8')
    for ip in ips:
        start_ip = ip.get('start_ip')
        end_ip = ip.get('end_ip')
        t_ips = math_ip_list(start_ip,end_ip)
        for t_ip in t_ips:
            file.write(t_ip+"\n")
    file.close()