
import subprocess
import sys



#data_path = "/home/qiqi/test1/test4"
white_list = 'white.txt'

def port_scan(task_id, data_path, port):
    filename = data_path+task_id+'.txt'
    cmd = ['zmap', '-B', '1M', '-p', port, '-o', filename, '-w', data_path+white_list]
    subprocess.Popen(cmd).communicate()


def protocol_detect(task_id, data_path, port, scan_type='', script=''):
    tmp_filename = data_path+task_id+'.txt'
    res_filename = data_path+task_id+'.xml'
    zmap_cmd = ['zmap', '-B', '1M', '-p', port, '-w', data_path+white_list, '-o', tmp_filename]
    if scan_type != '':
        scan_type = scan_type + ' '
    if script != '':
        script =' --script '+data_path+script+' '
    nmap_cmd = 'nmap -Pn ' + scan_type + script + '-p ' + port + ' -iL ' + tmp_filename + ' -oX ' + res_filename
    zmap_child = subprocess.Popen(zmap_cmd)
    zmap_child.communicate()
    subprocess.Popen(nmap_cmd, shell=True).communicate()  # 如果有stdout=PIPE则必需nmap_child.communicate()才可执行不然


def main(flag):
    if flag == 'port_scan':
        port_scan(sys.argv[2], sys.argv[3], sys.argv[4])
    elif flag == 'protocol_sniffer':
        protocol_detect(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    else:
        print('please select scan strategy')



if __name__ == '__main__':
    main(sys.argv[1])


