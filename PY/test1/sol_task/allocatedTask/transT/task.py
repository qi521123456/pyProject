import os,re,sys

protocolList = ["rtsp","S7Comm","EtherNetIP","Modbus"]
portList = ["80","21"]
tests = ["test1","test2","test3"]
path = "/home/mannix/"
def main(node):
    for test in tests:
        filedir = path+test+"/"
        for filename in os.listdir(filedir):
            if re.match('^1.*txt$', filename) is None:
                #os.system("rm -rf %s"%filedir+filename)
                print("rm -rf %s"%filedir+filename)
        for protocol in protocolList:
            cmd = "nohup docker run -v /root/data:/data tmpnmap python /data/newscan.py --test=" + test + " --country=h --node="+node+" --protocol="+protocol + "> /dev/null 2>&1 &"
            #os.popen(cmd)
            print(cmd)
        for port in portList:
            cmd = "nohup docker run -v /root/data:/data tmpnmap python /data/newscan.py --test=" + test + " --country=h --node="+node+" --port=" + port + "> /dev/null 2>&1 &"
            #os.popen(cmd)
            print(cmd)





if __name__ == '__main__':
    main(sys.argv[1])