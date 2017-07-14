import os,time
for i in range(3,11):
    if i==7 or i==8:
        continue
    try:
        host = "vps"+str(i)
        # info = os.popen("ssh " + host + " 'ps aux|grep python3'")
        # time.sleep(1)
        # os.popen("ssh " + host + " 'rm -rf /opt/*'")
        # time.sleep(1)
        # os.popen("scp -r /root/lmq/* root@%s:/opt/" % host)
        time.sleep(1)
        os.popen("ssh "+ host + " 'nohup python3 /opt/sol_netscan/net_sniffer.py > /dev/null 2>&1 &'")
        time.sleep(1)
        os.popen("ssh " + host + " 'nohup python3 /opt/sol_netscan2/net_sniffer2.py > /dev/null 2>&1 &'")
        time.sleep(1)
        os.popen("ssh " + host + " 'nohup python3 /opt/sol_netscan3/net_sniffer3.py > /dev/null 2>&1 &'")
    except:
        print(i,"--wrong--")


