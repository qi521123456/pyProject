import os,time
for i in range(2,11):
    try:
        host = "vps"+str(i)
        # info = os.popen("ssh " + host + " 'ps aux|grep python3'")
        # time.sleep(1)
        # os.popen("ssh " + host + " 'rm /opt/sol_netscan/utils*'")
        # time.sleep(1)
        # os.popen("scp /root/temp/* root@%s:/opt/sol_netscan/" % host)
        time.sleep(1)
        os.popen("ssh "+ host + " 'nohup python3 /opt/sol_netscan/net_sniffer.py > /dev/null 2>&1 &'")
    except:
        print(i,"--wrong--")

