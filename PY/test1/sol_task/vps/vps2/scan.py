import subprocess
import sys
import os

white_list = 'white.txt'


def port_scan(task_id, task_path, port):
    target_file = task_path+task_id+'.txt'
    cmd = ['zmap', '-B', '1M', '-p', port, '-o', target_file, '-w', task_path+white_list]
    os.system("/sbin/ldconfig")
    subprocess.Popen(cmd).communicate()


def protocol_detect(task_id, task_path, protocols):
    protocols = eval(protocols)
    for protocol in protocols:
        port_type = protocol.get('portType')
        port = protocol.get('protocolPort')
        protocol_name = protocol.get('protocolName')
        tmp_filename = task_path+task_id+'.txt'
        res_filename = task_path+task_id+"_"+protocol_name+'.xml'
        zmap_cmd = ['zmap', '-B', '1M', '-p', port, '-w', task_path+white_list, '-o', tmp_filename]
        if port_type == 'TCP':
            scan_type = '-sS'
        else:
            scan_type = '-sU'
        script = task_path+protocol_name+".nse"
        nmap_cmd = ['nmap','-Pn',scan_type,'--script',script,'-p',port,'-iL',tmp_filename,'-oX',res_filename]
        #nmap_cmd = "nmap -Pn %s --script %s -p %s -iL %s -oX %s" % (scan_type,script,port,tmp_filename,res_filename)
        zmap_child = subprocess.Popen(zmap_cmd)
        zmap_child.communicate()
        subprocess.Popen(nmap_cmd, shell=True).communicate()


if __name__ == '__main__':
    args = sys.argv
    if args[1] == 'port_scan':
        port_scan(args[2],args[3],args[4])
    elif args[1] == 'protocol_sniffer':
        protocol_detect(args[2], args[3], args[4])
    else:
        print('please select scan strategy')

