
import dpkt
f = open('/home/mannix/Desktop/79.143.87.223-1.cap','rb')

pacp = dpkt.pcap.Reader(f)
dpktEth = dpkt.ethernet
dpktDns = dpkt.dns
pkts_num =0
pkts_len=[]
for Pkt in pacp:
    eth = dpktEth.Ethernet(Pkt[1])
    print(type(eth))
    print(type(eth.data))
    print(type(eth.data.data))
    print(type(eth.data.data.data))
    udp = eth.data.data
    if not isinstance(udp,dpkt.udp.UDP):
        continue
    dns = udp.data
    a = dpktDns.DNS(dns)
    print(type(a))
    url = a.qd[0].name
    print(len('.'.join(str(url).split('.')[:-2]))<15)
    # print(''.join(map(lambda x:('/x' if len(hex(x))>=4 else '/x0')+hex(x)[2:],eth.data.data.data)))
    pkts_num += 1
#print pkts_len
print('PKTs：%d' % pkts_num)