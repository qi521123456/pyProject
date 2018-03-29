import subprocess
import sys
import os

white_list = 'white.txt'


def _localAddr():
    try:
        c = os.popen("env|grep hostip")
        s = c.read().split("=")
        ip = s[1].strip()
        mc = os.popen("env|grep mac")
        mac = mc.read().split("=")[1].strip()
    except:
        ip = '127.0.0.1'
        mac = '02:42:f1:ce:03:eb'
    return str(ip), str(mac)
IP,MAC = _localAddr()
SNMP_CMD = "zmap -M udp -B 1M -p 161 --probe-args=hex:302702010004067075626c6963a01a02026f0c020100020100300e300c06082b060102010101000500 -f saddr"
BACnet_CMD = "zmap -M udp -B 1M -p 47808 --probe-args=hex:810a001101040005010c0c023FFFFF194b -f saddr"
MOXA_CMD = "zmap -M udp -B 1M -p 4800 --probe-args=hex:0100000800000000 -f saddr"
def _zmap_command(port,target_file,white):
    port = str(port)
    if port == "161":
        cmd = SNMP_CMD.split(" ")
    elif port == "47808":
        cmd = BACnet_CMD.split(" ")
    elif port == "4800":
        cmd = MOXA_CMD.split(" ")
    else:
        cmd = ['zmap', '-B', '1M', '-G', MAC, '-p', port]
    cmd.append("-o")
    cmd.append(target_file)
    cmd.append("-w")
    cmd.append(white)
    os.system("/sbin/ldconfig")
    return cmd

def port_scan(task_id, task_path, port):
    target_file = task_path+task_id+'.txt'
    # cmd = ['zmap', '-B', '1M', '-p', port, '-o', target_file, '-w', task_path+white_list]
    cmd = _zmap_command(port,target_file,task_path+white_list)
    subprocess.Popen(cmd, close_fds=True, preexec_fn=os.setpgrp).communicate()


def protocol_detect(task_id, task_path, protocols):
    protocols = eval(protocols)
    for protocol in protocols:
        port_type = protocol.get('portType')
        port = protocol.get('protocolPort')
        protocol_name = protocol.get('protocolName')
        tmp_filename = task_path+task_id+'.txt'
        res_filename = task_path+task_id+"_"+protocol_name+'.xml'
        # zmap_cmd = ['zmap', '-B', '1M', '-p', port, '-w', task_path+white_list, '-o', tmp_filename]
        zmap_cmd = _zmap_command(port,tmp_filename,task_path+white_list)
        if port_type == 'TCP':
            scan_type = '-sS'
        else:
            scan_type = '-sU'
        script = task_path+protocol_name+".nse"
        nmap_cmd = ['nmap','-Pn',scan_type,'--script',script,'-p',port,'-iL',tmp_filename,'-oX',res_filename]
        #nmap_cmd = "nmap -Pn %s --script %s -p %s -iL %s -oX %s" % (scan_type,script,port,tmp_filename,res_filename)
        zmap_child = subprocess.Popen(zmap_cmd, close_fds=True, preexec_fn=os.setpgrp)
        zmap_child.communicate()
        subprocess.Popen(nmap_cmd, close_fds=True, preexec_fn=os.setpgrp).communicate()


if __name__ == '__main__':
    args = sys.argv
    if args[1] == 'port_scan':
        port_scan(args[2],args[3],args[4])
    elif args[1] == 'protocol_sniffer':
        protocol_detect(args[2], args[3], args[4])
    else:
        print('please select scan strategy')

