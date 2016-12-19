
import subprocess
import sys
from optparse import OptionParser


#data_path = "/home/qiqi/test1/test4"
white_list = 'white.txt'

def port_scan(task_id, data_path, port):
    filename = data_path+task_id+'.txt'
    cmd = 'zmap -p '+port+' -o '+filename+' -w '+data_path+white_list
    subprocess.Popen(cmd, shell=True)  # shell=True 才可运行string否则只能以列表形式写入cmd


def protocol_detect(task_id, data_path, port, scan_type='', script=''):
    tmp_filename = data_path+task_id+'.txt'
    res_filename = data_path+task_id+'.xml'
    zmap_cmd = 'zmap -p '+port+' -w '+data_path+white_list+' -o '+tmp_filename
    if scan_type != '':
        scan_type = scan_type + ' '
    if script != '':
        script =' --script '+data_path+script+' '
    nmap_cmd = 'nmap ' + scan_type + script + '-p ' + port + ' -iL ' + tmp_filename + ' -oX ' + res_filename
    print(nmap_cmd)
    zmap_child = subprocess.Popen(zmap_cmd, shell=True)
    zmap_child.communicate()
    subprocess.Popen(nmap_cmd, shell=True)  # 如果有stdout=PIPE则必需nmap_child.communicate()才可执行不然


def main(flag):
    usage = "python %proc [options] args"
    if flag == 'port_scan':
        usage = "python %proc port_scan [ -id <task_id>] [-dp <data_path>] [-p <port>]"
        port_scan(sys.argv[2], sys.argv[3], sys.argv[4])
    elif flag == 'protocol_detect':
        usage = "python %proc protocol_detect [ -id <task_id>] [-dp <data_path>] [-p <port>] [-st <scan_type>] [-script <script>]"
        protocol_detect(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    else:
        print('please select scan strategy')
    parser = OptionParser(usage)


if __name__ == '__main__':
    main(sys.argv[1])


