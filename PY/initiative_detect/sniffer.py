try:
    import os
    import re
    import time
    import docker
    import xml.etree.cElementTree as ET
except Exception as ex:
    print(ex)
    exit()

Protocol = [
    {"protocol": "S7Comm", "port": 102},
    {"protocol": "Modbus", "port": 502},
    {"protocol": "EtherNetIP", "port": 44818},
    {"protocol": "Fox", "port": 1911},
    {"protocol": "DNP3", "port": 20000},
    {"protocol": "Cspv4", "port": 2222},
    {"protocol": "SNMP", "port": 161,"type":"UDP"},
    {"protocol": "BACnet", "port": 47808,"type":"UDP"},
    {"protocol": "FINS-TCP","port":9600},
    {"protocol": "FINS-UDP","port":9600,"type":"UDP"},
    {"protocol": "MELSEC-Q-TCP","port":5007},
    {"protocol": "MELSEC-Q-UDP","port":5006,"type":"UDP"},
    {'protocol': "HTTP","port":80},
    {'protocol': "IEC-104","port":2404}
]

Province = [
    "BeiJing", "ShanDong", "TaiWan", "JiLin", "SiChuan", "HeiLongJiang",
    "LiaoNing", "HeBei", "HeNan", "GuangDong", "ShangHai", "Shan3Xi",
    "JiangSu", "AnHui", "TianJin", "GanSu", "FuJian", "ZheJiang",
    "ShanXi", "YunNan", "HaiNan", "GuangXi", "HuBei", "HuNan",
    "GuiZhou", "NeiMeng", "XiangGang", "AoMen", "ChongQing", "JiangXi",
    "QingHai", "NingXia", "XinJiang", "XiZang"
]

GATE_WAY = "56:84:7a:fe:97:99"
SCRIPT = "/data/Script/"
SRC_IP = "/data/ChinaIP/"
DST_FILE = "/data/auto/"
TARGET = "/data/target/"

SNMP_CMD = "zmap -M udp -B 1M -p 161 --probe-args=hex:302702010004067075626c6963a01a02026f0c020100020100300e300c06082b060102010101000500 -f saddr"
BACnet_CMD = "zmap -M udp -B 1M -p 47808 --probe-args=hex:810a001101040005010c0c023FFFFF194b -f saddr"
FINS_CMD = "zmap -M udp -B 1M -p 9600 --probe-args=hex:800002000000006300ef050100 -f saddr"
MELSEC_Q_CMD = "zmap -M udp -B 1M -p 5006 --probe-args=hex:57000000001111070000ffff030000fe03000014001c080a0800000000000000040101010000000001 -f saddr"

class XMLHandler:
    def __init__(self,file):
        try:
            self.file = file
            self.tree = ET.parse(file)
        except Exception as e:
            print(e)

    def get_root(self):
        return self.tree.getroot()

    def get_elements(self,element,xpath):
        return element.findall(xpath)

    def get_element(self,element,xpath):
        return element.find(xpath)

    def get_element_value(self,element):
        return element.text

    def get_attr_value_by_name(self,element,attr_name):
        return element.get(attr_name)

    def get_attributes(self,element):
        return element.items()

    def update_attribute(self,element,attribute,value):
        element.set(attribute,value)

    def update_text(self,element,value):
        element.text = value

    def add_child(self,parent,child_tag,child_text):
        child = ET.SubElement(parent,child_tag)
        child.text = child_text
        return child

    def del_child(self,parent,child):
        parent.remove(child)

    def get_children(self,element,tag=None):
        return element.iter(tag)

    def clear_element(self,element):
        element.clear()

    def save(self):
        self.tree.write(self.file,encoding="UTF-8",xml_declaration=True)


def get_specific_ip(network_device):
    def parse_ip(command):
        pattern = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        ips = pattern.findall(command)
        return ips[0] if ips else None
    ip_info = os.popen('ifconfig').read()
    device_index = ip_info.find(network_device)
    if device_index != -1:
        line = ip_info[device_index:len(ip_info)]
        ip = parse_ip(line)
        return ip if ip else None
    else:
        return None


def running_containers():
    client = docker.Client(base_url='unix://var/run/docker.sock',version='1.9',timeout=10)
    return len(client.containers())

def verify_port(port_file):
    try:
        ips = list()
        with open(port_file,'r') as f:
            line = f.readline()
            while True:
                if not line:
                    break
                if len(line.split('.')) is 4:
                    line = line[:-1]
                    ips.append(line)
                line = f.readline()
        with open(port_file,'w') as f:
            for ip in ips:
                f.write(ip+"\n")
    except Exception as ex:
        print(ex)

def get_open_port_ip(file):
    open_ip_list = list()
    xml_handler = XMLHandler(file)
    hosts = xml_handler.get_elements(xml_handler.get_root(),'host')
    for host in hosts:
        address = xml_handler.get_element(host,'address')
        ip = xml_handler.get_attr_value_by_name(address,'addr')
        ports = xml_handler.get_element(host,'ports')
        for port in ports:
            e_state = xml_handler.get_element(port,'state')
            state = xml_handler.get_attr_value_by_name(e_state,'state')
            if state != 'closed':
                open_ip_list.append(ip)
                break
    new_file = os.path.splitext(file)[0] + ".txt"
    with open(new_file,'w') as f:
        for ip in open_ip_list:
            f.write(ip+"\n")


def run_port_scan(protocol, location):
    try:
        docker_cmd = "docker run -d -v /home:/data --privileged sniffer"
        for i in range(3):  # 3个文件
            src_file = "%s%s_%s.txt" % (SRC_IP, location, str(i+1))
            dst_file = "%s%s_%s_%s.txt" % (DST_FILE, location, protocol.get('protocol'), str(i+1))
            if protocol.get('type') is None:
                zmap_cmd = "zmap -B 1M -p %s -w %s -o %s -G %s" % (str(protocol.get('port')), src_file, dst_file, GATE_WAY)
            else:
                if protocol.get('protocol') == 'SNMP':
                    zmap_cmd = "%s -w %s -o %s -G %s" % (SNMP_CMD,  src_file, dst_file, GATE_WAY)
                elif protocol.get('protocol') == 'BACnet':
                    zmap_cmd = "%s -w %s -o %s -G %s" % (BACnet_CMD,  src_file, dst_file, GATE_WAY)
                elif protocol.get('protocol') == 'FINS':
                    zmap_cmd = "%s -w %s -o %s -G %s" % (FINS_CMD,  src_file, dst_file, GATE_WAY)
                else:
                    zmap_cmd = "%s -w %s -o %s -G %s" % (MELSEC_Q_CMD,  src_file, dst_file, GATE_WAY)
            cmd = "%s %s" % (docker_cmd, zmap_cmd)
            os.system(cmd)
            time.sleep(10)
    except Exception as ex:
        print("run_port_scan:" + str(ex))


def run_script_scan(protocol, location):
    try:
        docker_cmd = "docker run -d -v /home:/data --privileged sniffer"
        flag = True
        for i in range(3):
            src_file = "%s%s_%s_%s.txt" % (DST_FILE,location,protocol.get('protocol'),str(i+1))
            #verify_port(src_file)
            dst_file = "%s%s_%s_%s.xml" % (DST_FILE,location,protocol.get('protocol'),str(i+1))
            if protocol.get('type') is None:
                nmap_cmd = "nmap --script %s%s.nse -Pn -sS -p %s -iL %s -oX %s" % (SCRIPT,protocol.get('protocol'),str(protocol.get('port')),src_file,dst_file)
            else:
                nmap_cmd = "nmap --script %s%s.nse -Pn -sU -p %s -iL %s -oX %s" % (SCRIPT,protocol.get('protocol'),str(protocol.get('port')),src_file,dst_file)
            cmd = "%s %s" % (docker_cmd,nmap_cmd)
            os.system(cmd)
            time.sleep(10)
    except Exception as ex:
        print("run_script_scan:" + str(ex))


def run_scan(location, protocol_index):
    try:
        if location not in Province:
            print("Invalid location")
            return
        protocols = Protocol[protocol_index:]
        while True:
            while running_containers() != 0:
                time.sleep(60 * 5)
            if len(protocols) is 0:
                break
            os.system("docker rm -f $(docker ps -aq)")
            protocol = protocols.pop(0)
            run_port_scan(protocol, location)
            while running_containers() != 0:
                time.sleep(60 * 5)
            run_script_scan(protocol, location)
    except Exception as e:
        print("run_scan:" + str(e))

def province_scan(start_index):
    try:
        provinces = Province[start_index:]
        province = None
        while True:
            if len(provinces) is 0:
                break
            if running_containers() is 0:
                province = provinces.pop(0)
                run_scan(province, 0)
            else:
                time.sleep(60 * 5)
    except Exception as e:
        print("province_scan:" + str(e))

if __name__ == '__main__':
    import sys
    args = sys.argv
    if len(args) is 2:
        province_scan(int(args[1]))
    elif len(args) is 3:
        run_scan(args[1], int(args[2]))
    else:
        pass
