
filename = "D:/test_e/ttt.txt"
ip_src = ["111.5.2.4/8\n","222.2.2.2/8\n"]
# for i in range(5):
#     with open(filename+'.txt','w') as ips:
#         #ips.write(r"eee\r\nrrr")
#         ips.writelines(ip_src)
#         #ips.close()
#         ips.close()

def afterClose(file): # 当ijson时不行，因为流输入
    with open(file,'r') as f:
        data = f.read()
        f.close()
    return data

# print(afterClose("D:/HTTP.nse"))
def writetest(file):
    with open(file,'w') as fw:
        fw.writelines(i+'\n' for i in ['w','ee'])

writetest(filename)