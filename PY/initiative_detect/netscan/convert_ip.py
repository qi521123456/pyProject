from functools import reduce
from IPy import IP,IPSet
from utils.mongodb import MongoDBInterface

def get_common_len(number_a,number_b):
    number_a = bin(int(number_a)).replace('0b','')
    number_b = bin(int(number_b)).replace('0b','')
    number_a = number_a if len(number_a) is 8 else ('0' * (8-len(number_a)) + number_a)
    number_b = number_b if len(number_b) is 8 else ('0' * (8-len(number_b)) + number_b)
    index = 0
    while index < 8:
        if number_a[index] == number_b[index]:
            index+=1
        else:
            return index

def get_common_ip(ip_a,ip_b):
    if ip_a == ip_b:
        return ip_a
    ip_a = ip_a.split('.')
    ip_b = ip_b.split('.')
    start = 0
    while start < 4:
        if ip_a[start] == ip_b[start]:
            start+=1
        else:
            break
    part_len = get_common_len(ip_a[start],ip_b[start])
    prefix = 8 * start + part_len
    base_number = bin(int(ip_a[start])).replace('0b','')
    base_number = base_number if len(base_number) is 8 else ('0' * (8-len(base_number)) + base_number)
    base_number = str(base_number)[:part_len]
    base_power = list(map(lambda x:pow(2,(8-x-1)),range(part_len)))
    part_number = 0
    for i in range(len(base_number)):
        part_number+=(int(base_number[i]) * base_power[i])
    #part_number = str(reduce(lambda x,y:x+y,map(lambda x:pow(2,(8-x-1)),range(part_len))))
    ip_a[start] = str(part_number)
    start+=1
    while start < 4:
        ip_a[start] = "0"
        start+=1
    return '.'.join(ip_a)+"/%s"%str(prefix)

def ip_parse(ip_a,ip_b):
    target = None
    try:
        temp = "%s-%s" % (ip_a,ip_b)
        target = IP(temp)
    except:
        target = get_common_ip(ip_a,ip_b)
    finally:
        return str(target)

"""
江西
天津 江苏 安徽 福建 贵州 云南 青海 新疆
"""
if __name__ == '__main__':
    mi = MongoDBInterface()
    mi.connect('localhost','SOL','root','Free-Wi11')
    res = mi.query(None,'ChinaIP',{'province':'湖北'})
    res = res[0].get('ips')
    with open('d:\ChinaIP\HuBei.txt','w+',encoding='UTF-8') as f:
        for item in res:
            target = ip_parse(item.get('start_ip'),item.get('end_ip'))
            f.write(target+"\n")