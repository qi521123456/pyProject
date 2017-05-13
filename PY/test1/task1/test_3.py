# coding utf-8
import struct,socket
def ip2long(ip):
    packedIP=socket.inet_aton(ip)
    return struct.unpack("!L",packedIP)[0]
def long2ip(longNum):
    return socket.inet_ntoa(struct.pack('!L',longNum))
print(str(ip2long("87.241.191.255"))+"\n"+str(long2ip(2130706433)))

def ch1(num):
    s = []
    for i in range(4):
        s.append(str(int(num % 256)))
        num /= 256
        print(i)
    print(s)
    return '-'.join(s[::-1])
#print(ch1(123456789))