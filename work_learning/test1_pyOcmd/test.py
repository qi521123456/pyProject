def ipform(ips):
    ip = ips
    if ips.find('/') != -1:
        str1 = ips.split('/')
        if -1 < int(str1[1]) < 33:
            ip = str1[0]
        else:
            print('error targets')
            return False
    str2 = ip.split('.')
    for i in str2:  # TODO
        if int(i) < 0 or int(i) > 255:
            return False
    return True
#print(ipform('127.0.0.33'))
# i = ('222',3)
# print(str(i[1])+' '+i[0])

print('wea sa efef w'.replace('  ',' '))