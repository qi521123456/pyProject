
filename = "D:/test_e/ttt"
ip_src = ["111.5.2.4/8\n","222.2.2.2/8\n"]
for i in range(5):
    with open(filename+'.txt','w') as ips:
        #ips.write(r"eee\r\nrrr")
        ips.writelines(ip_src)
        #ips.close()
        ips.close()