import os,time
from kazoo.client import KazooClient
# for i in range(3,11):
#     try:
#         host = "vps"+str(i)
#         info1 = os.popen("ssh "+host+" 'mv /opt/sol_netscan/net_sniffer.py /opt/sol_netscan/net_sniffer.py.bak'")
#         info2 = os.popen("ssh " + host + " 'mv /opt/sol_netscan/utils.py /opt/sol_netscan/utils.py.bak'")
#         info3 = os.popen("scp /root/temp/* root@%s:/opt/sol_netscan/")
#     except:
#         print(i,"--wrong--")

