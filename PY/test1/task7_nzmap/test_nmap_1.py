import os
import subprocess
from libnmap.process import NmapProcess

def scan_by_ip(ip):
    lines = os.popen(r'nmap -sT '+ip).readlines()
    for line in lines:
        print(line+'\n')
def scan_ip(ip):
    p = subprocess.Popen(r'nmap -sT '+ip, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print(line.decode('gb2312')+r'---\n')



if __name__ == '__main__':
    #scan_by_ip('10.0.1.122')
    #scan_ip('10.0.10.167')
    p = subprocess.Popen(r'ping baidu.com', shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(p.poll())
    # p.kill()
    #print(p.stdout.readlines())
    try:
        o ,e = p.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        p.kill()
        o,e = p.communicate()
    print(NmapProcess(targets='10.0.10.167',options='-sT'),p.pid,p.poll(),p)
    print(o.decode('gb2312'))
