try:
    from utils.mysql import MysqlInterface
    from utils.configure import DataBase
    from utils.logging import Logging
    from utils.xml import XMLHandler
    from kazoo.client import KazooClient
    from functools import reduce
    import geoip2.database
    import datetime
    import requests
    import zipfile
    import socket
    import struct
    import time
    import os
    import re
except Exception as ex:
    print(ex)


class Province:
    PROVINCES = [
        "北京", "天津", "上海", "重庆", "河北",
        "河南", "云南", "辽宁", "黑龙江", "湖南",
        "安徽", "山东", "新疆", "江苏", "浙江",
        "江西", "湖北", "广西", "甘肃", "山西",
        "内蒙古", "陕西", "吉林", "福建", "贵州",
        "广东", "青海", "西藏", "四川", "宁夏",
        "海南", "台湾", "香港", "澳门"
    ]

    @classmethod
    def init_province(cls):
        return {item: {} for item in cls.PROVINCES}


def get_mysql_connect():  # get mysql connect, add by lhb
    #print("get mysql connect...")
    conn = MysqlInterface(host=DataBase.db_host, user=DataBase.db_user, password=DataBase.db_pass, db=DataBase.db_name)
    return conn


class FlowAnalyzer:

    def file_iterator(self, file_name, seperator):
        try:
            file = open(file_name,'r',encoding='UTF-8')
        except FileNotFoundError as fne:
            print(fne)
            return
        else:
            f_line = file.readline()
            while True:
                if not f_line:
                    break
                line_items = f_line.split(seperator)
                yield line_items
                f_line = file.readline()

    def save_file(self, file_name, data_source):
        if type(data_source) is not list:
            print("data source invalid")
        else:
            with open(file_name,'w+',encoding='UTF-8') as fp:
                for data in data_source:
                    fp.write(data+"\n")

    def extract_snmp_figger(self, device_info):
        device_figger = dict()
        try:
            if 'Siemens' in device_info:
                device_figger['figger'] = device_info.strip()[device_info.find('Siemens'):]
            elif 'Rockwell' in device_info:
                device_figger['figger'] = device_info.strip()[device_info.find('Rockwell'):]
            elif 'Schenider' in device_info:
                device_figger['figger'] = device_info.strip()[device_info.find('Schenider'):]
        except:
            pass
        finally:
            return device_figger

    def extract_ip(self, src_file):
        ip_list = list()
        try:
            xml_handler = XMLHandler(src_file)
            host_elements = xml_handler.get_elements(xml_handler.get_root(),"host")
            for host_element in host_elements:
                host_ports = xml_handler.get_element(host_element,'ports')
                for host_port in host_ports:
                    script = xml_handler.get_element(host_port,'script')
                    if script is None:
                        continue
                    address_ele = xml_handler.get_element(host_element,'address')
                    address = xml_handler.get_attr_value_by_name(address_ele,'addr')
                    ip_list.append(address) if address not in ip_list else ""
        except:
            pass
        finally:
            return ip_list


class NetScan:

    Logger = Logging().get_logger()

    @classmethod
    def get_ip_list(cls, file):
        ip_list = list()
        try:
            file_opener = open(file,encoding="UTF-8")
        except FileNotFoundError:
            cls.Logger.error("File not found")
        else:
            cursor = file_opener.readline()
            while True:
                if not cursor:
                    break
                cursor = cursor.strip()[0:len(cursor)-1] if "\n" in cursor else cursor.strip()
                ip_list.append(cursor)
                cursor = file_opener.readline()
        return ip_list

    @classmethod
    def extract_fingger(cls, scan_file, protocol=None):
        scan_result = []
        try:
            handler = XMLHandler(scan_file)
            host_elements = handler.get_elements(handler.get_root(),"host")
            for host_element in host_elements:
                target_elements = handler.get_elements(host_element,"ports/port/script")
                if target_elements is None or len(target_elements) is 0:
                    continue
                address_element = handler.get_element(host_element,"address")
                address = handler.get_attr_value_by_name(address_element,"addr")
                for target_element in target_elements:
                    elem_elements = handler.get_elements(target_element,"elem")
                    if elem_elements is None or len(elem_elements) is 0:
                        continue
                    fingerprint = dict()
                    for elem in elem_elements:
                        if protocol == "FINS":
                            elem_key = handler.get_attr_value_by_name(elem,"key")
                            elem_key = elem_key.replace('.',"") if '.' in elem_key else elem_key
                            if elem_key == 'Controller Model':
                                fingerprint[elem_key] = handler.get_element_value(elem).split(" ")[0]
                            else:
                                fingerprint[elem_key] = handler.get_element_value(elem)
                        elif protocol == "SNMP":
                            elem_key = handler.get_attr_value_by_name(elem,"key")
                            elem_value = handler.get_element_value(elem)
                            if 'Siemens' in elem_value or 'Rockwell' in elem_value or 'Schenider' in elem_value:
                                fingerprint = FlowAnalyzer().extract_snmp_figger(handler.get_element_value(elem))
                        else:
                            fingerprint[handler.get_attr_value_by_name(elem,"key")] = handler.get_element_value(elem)
                    if len(fingerprint) is 0:
                        pass
                    else:
                        scan_item = {"ip":address,"result":fingerprint}
                        scan_result.append(scan_item)
        except:
            pass
        return scan_result

    @classmethod
    def echo_targets(cls, d_targets):
        """格式化输出扫描结果"""
        try:
            for k_province in d_targets:
                ip_area = d_targets.get(k_province)
                for area in ip_area:
                    print(area)
                    for ip_addr in ip_area.get(area):
                        print(ip_addr)
        except:
            cls.Logger.warning("")

    @classmethod
    def get_lng_lat(cls, ip):
        try:
            reader = geoip2.database.Reader(r'file/GeoLite2-City.mmdb')
            response = reader.city(ip)
            return [response.location.longitude,response.location.latitude]
        except Exception as e:
            cls.Logger.error(e)

    @classmethod
    def total_results(cls, dir_path, protocol=None, extension="xml"):
        if not os.path.isdir(dir_path):
            cls.Logger.warning("Invalid Path")
            return
        l_file = os.listdir(dir_path)
        t_results = list()
        for s_file in l_file:
            if os.path.isfile(dir_path+"/" + s_file) is False:
                continue
            if len(os.path.splitext(s_file)) < 2:
                continue
            if os.path.splitext(s_file)[1][1:] != extension:
                continue

            sub_path = dir_path + "/" + s_file
            with open(sub_path, mode='r+') as f:
                datas = f.read()
                if '</nmaprun>' not in datas:
                    f.write('</nmaprun>')

            s_results = cls.extract_fingger(dir_path+"/" + s_file, protocol)
            for s_result in s_results:
                flag = True
                s_ip = s_result.get('ip')
                for t_result in t_results:
                    if t_result.get('ip') == s_ip:
                        flag = False
                if flag:
                    t_results.append(s_result)
        return t_results

    @classmethod
    def query_target(cls, target, ip_list):
        target = socket.ntohl(struct.unpack("I", socket.inet_aton(target))[0])
        low, high = 0, len(ip_list)-1
        mid = 0
        while low <= high:
            mid = (low+high) // 2
            if ip_list[mid] <= target < ip_list[mid+1]:
                return ip_list[mid]
            elif target < ip_list[mid]:
                high = mid - 1
            else:
                low = mid + 1
        return -1

    @classmethod
    def get_locations(cls, connect=None):
        if connect is None:
            return None
        ip_list = list()
        locations = dict()
        try:
            query_sql = "SELECT ip_from,country,province,city FROM ip_ipipnet"
            query_res = connect.query(query_sql)
            for item in query_res:
                ip_list.append(item.get('ip_from'))
                locations[item.get('ip_from')] = dict()
                locations[item.get('ip_from')]['country'] = item.get('country')
                locations[item.get('ip_from')]['province'] = item.get('province')
                locations[item.get('ip_from')]['city'] = item.get('city')
        except Exception as ex:
            print(ex)
        return ip_list, locations

    @classmethod
    def filter_results(cls, res, conn=None, **kwargs):
        filtered_res = []
        ip_list, locations = cls.get_locations(conn)
        for result in res:
            ip = result.get('ip')
            ip_location = locations.get(cls.query_target(ip, ip_list))
            lng_lat = cls.get_lng_lat(result.get('ip'))
            result["geo"] = lng_lat
            result["location"] = ip_location
            if kwargs.get("protocol") is not None:
                result["protocol"] = kwargs.get("protocol")
            if kwargs.get("timestamp") is not None:
                result["timestamp"] = kwargs.get("timestamp")
            filtered_res.append(result)
        return filtered_res


def s7comm_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    # res = NetScan.total_results('D:\Res\Res', protocol='S7Comm')
    res = NetScan.total_results(dir_path, protocol='S7Comm')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res, conn=mysql_connect, protocol='S7Comm', timestamp=create_time)
    if len(res) == 0:
        return
    print("res nums:" + str(len(res)))
    for item in res:
        if item.get('location') is None:
            continue
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        basic_hardware = result.get('Basic Hardware')
        system_name = result.get('System Name')
        module_type = result.get('Module Type')
        module = result.get('Module')
        version = result.get('Version')
        serial_number = result.get('Serial Number')
        copyright = result.get('Copyright')
        vendor = 'Siemens'
        insert_sql ="INSERT INTO `result_s7comm`" \
                    "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `basic_hardware`, `system_name`, `module_type`, `module`, `version`, `serial_number`, `copyright`, `longitude`, `latitude`,`node_id`,`script_id`,`protocol_id`)" \
                    " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                    % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor, basic_hardware, system_name, module_type, module, version, serial_number, copyright, longitude, latitude, node_id, script_id, protocol_id)
        # print("-----------------",insert_sql)
        mysql_connect.insert(insert_sql)

def modbus_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):  # result into mysql directly
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='Modbus')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res, conn=mysql_connect, protocol='Modbus', timestamp=create_time)
    print("get filter res")
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        vendor = result.get('Vendor')
        revision = result.get('Revision')
        device = result.get('Device')
        if vendor == 'Siemens':  # 特殊判断
            if revision is not None:
                device = device + ' ' + revision
                revision = None
        insert_sql ="INSERT INTO `result_modbus`" \
                    "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `revision`, `device`, `longitude`, `latitude`,`node_id`,`script_id`,`protocol_id`)" \
                    " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')" \
                    % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor, revision, device, longitude, latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def ethernetip_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='EtherNetIP')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res, conn=mysql_connect, protocol='EtherNetIP', timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        vendor = result.get('Vendor')
        product_name = result.get('Product Name')
        serial_number = result.get('Serial Number')
        device_type = result.get('Device Type')
        product_code = result.get('Product Code')
        revision = result.get('Revision')
        insert_sql ="INSERT INTO `result_ethernetip`" \
                    "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `product_name`, `serial_number`, `device_type`, `product_code`, `revision`, `longitude`, `latitude`,`node_id`,`script_id`,`protocol_id`)" \
                    " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                    % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor, product_name, serial_number,  device_type, product_code, revision, longitude, latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def fox_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='Fox')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res, conn=mysql_connect, protocol='Fox', timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        fox_version = result.get('Fox Version')
        host_name = result.get('Host Name')
        application_name = result.get('Application Name')
        application_version = result.get('Application Version')
        vm_name = result.get('VM Name')
        vm_version = result.get('VM Version')
        os_name = result.get('OS Name')
        time_zone = result.get('Time Zone')
        host_id = result.get('Host ID')
        vm_uuid = result.get('VM UUID')
        brand_id = result.get('Brand ID')
        insert_sql ="INSERT INTO `result_fox`" \
                    "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `fox_version`, `host_name`, `application_name`, `application_version`, `vm_name`, `vm_version`, `os_name`, `time_zone`, `host_id`, `vm_uuid`, `brand_id`, `longitude`, `latitude`,`node_id`,`script_id`,`protocol_id`)" \
                    " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                    % (task_id, create_time, device_ip, device_country, device_province, device_city, fox_version, host_name, application_name,  application_version, vm_name, vm_version, os_name, time_zone, host_id, vm_uuid, brand_id, longitude, latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def dnp3_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='DNP3')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res, conn=mysql_connect, protocol='DNP3', timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        destination_address = result.get('Destination Address')
        source_address = result.get('Source Address')
        control = result.get('Control')

        insert_sql = "INSERT INTO `result_dnp3`" \
                     "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `destination_address`, `source_address`, `control`, `longitude`, `latitude`, `node_id`, `script_id`, `protocol_id`)" \
                     " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s', '%s', '%s', '%s')" \
                     % (task_id, create_time, device_ip, device_country, device_province, device_city, destination_address, source_address, control, longitude, latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def cspv4_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='Cspv4')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res, conn=mysql_connect, protocol='Cspv4', timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        session_id = result.get('Session ID')

        insert_sql = "INSERT INTO `result_cspv4`" \
                     "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `session_id`, `longitude`, `latitude`, `node_id`, `script_id`, `protocol_id`)" \
                     " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (task_id, create_time, device_ip, device_country, device_province, device_city, session_id,
                        longitude, latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def snmp_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='SNMP')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res=res, conn=mysql_connect, protocol="SNMP", timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        figger = result.get('figger')
        if figger is not None:
            if figger.find('Siemens') is not -1:
                sie_res_list = figger.strip().split(',')
                if len(sie_res_list) == 7:
                    vendor = 'Siemens'
                    brand = sie_res_list[1].strip()
                    cpu = sie_res_list[2].strip()
                    order_no = sie_res_list[3].strip()
                    hardware_version = sie_res_list[4].strip()
                    fireware_version = sie_res_list[5].strip()
                    serial_number = sie_res_list[6].strip()
                elif len(sie_res_list) == 3:
                    vendor = 'Siemens'
                    brand = sie_res_list[1].strip()
                    cpu = sie_res_list[2].strip()
                    fireware_version = None
                    hardware_version = None
                    order_no = None
                    serial_number = None
                elif len(sie_res_list) == 6:
                    vendor = 'Siemens'
                    brand = sie_res_list[1].strip()
                    cpu = sie_res_list[2].strip()
                    order_no = sie_res_list[3].strip()
                    hardware_version = sie_res_list[4].strip()
                    serial_number = sie_res_list[5].strip()
                    fireware_version = None
            elif figger.find('Rockwell') is not -1:
                rock_res_list = figger.strip().split()
                vendor = 'Rockwell'
                brand = rock_res_list[1].strip()
                cpu = rock_res_list[2].strip()
                fireware_version = None
                hardware_version = None
                order_no = None
                serial_number = None
            else:
                continue
        else:
            vendor = result.get('Vendor')
            brand = result.get('System Name')
            cpu = result.get('Module Type')
            order_no = result.get('Basic Hardware')
            hardware_version = result.get('HW')
            fireware_version = result.get('FW')
            serial_number = result.get('Serial Number')

        insert_sql = "INSERT INTO `result_snmp`" \
                     "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `brand`, `cpu`, `fireware_version`, `hardware_version`, `order_no`, `serial_number`, `longitude`, `latitude`, `node_id`, `script_id`, `protocol_id`)" \
                     " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor, brand, cpu, fireware_version, hardware_version, order_no, serial_number, longitude, latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def bacnet_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='BACnet')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res, conn=mysql_connect, protocol='BACnet', timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        vendor_id = result.get('Vendor ID')
        vendor_name = result.get('Vendor Name')
        instance_number = result.get('Instance Number')
        firmware = result.get('Firmware')
        application_software = result.get('Application Software')
        object_name = result.get('Object Name')
        object_identifier = result.get('Object-identifier')
        model_name = result.get('Model Name')
        description = result.get('Description')
        location = result.get('Location')
        insert_sql ="INSERT INTO `result_bacnet`" \
                    "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor_id`, `vendor_name`, `instance_number`, `firmware`, `application_software`, `object_name`, `object_identifier`, `model_name`, `description`, `location`, `longitude`, `latitude`,`node_id`,`script_id`,`protocol_id`)" \
                    " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s')" \
                    % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor_id, vendor_name, instance_number, firmware, application_software, object_name, object_identifier, model_name, description, location, longitude, latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def fins_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):  # add by lhb
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='FINS')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res, conn=mysql_connect, protocol='FINS', timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        controller_model = result.get('Controller Model')
        controller_version = result.get('Controller Version')
        for_system_use = result.get('For System Use')
        program_area_size = result.get('Program Area Size')
        iom_size = result.get('IOM size')
        no_dm_words = result.get('No DM Words')
        timer_counter = result.get('Timer/Counter')
        expansion_dm_size = result.get('Expansion DM Size')
        no_of_steps_transitions = result.get('No of steps/transitions')
        kind_of_memory_card = result.get('Kind of Memory Card')
        memory_card_size = result.get('Memory Card Size')
        insert_sql ="INSERT INTO `result_fins`" \
                    "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `controller_model`, `controller_version`, `for_system_use`, `program_area_size`, `iom_size`, `no_dm_words`, `timer_counter`, `expansion_dm_size`, `no_of_steps_transitions`, `kind_of_memory_card`, `memory_card_size`, `longitude`, `latitude`, `node_id`, `script_id`, `protocol_id`)" \
                    " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                    % (task_id, create_time, device_ip, device_country, device_province, device_city, controller_model, controller_version, for_system_use, program_area_size, iom_size, no_dm_words, timer_counter, expansion_dm_size, no_of_steps_transitions, kind_of_memory_card, memory_card_size, longitude, latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def melsec_q_tcp_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='MELSEC-Q-TCP')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res=res, conn=mysql_connect, protocol="MELSEC-Q-TCP", timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        cpuinfo = result.get('CPUINFO')

        insert_sql = "INSERT INTO `result_melsec_q_tcp`" \
                     "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `cpuinfo`, `longitude`, `latitude`, `node_id`, `script_id`, `protocol_id`)" \
                     " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (
                     task_id, create_time, device_ip, device_country, device_province, device_city, cpuinfo, longitude,
                     latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def melsec_q_udp_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='MELSEC-Q-UDP')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res=res, conn=mysql_connect, protocol="MELSEC-Q-UDP", timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        cpuinfo = result.get('CPUINFO')

        insert_sql = "INSERT INTO `result_melsec_q_udp`" \
                     "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `cpuinfo`, `longitude`, `latitude`, `node_id`, `script_id`, `protocol_id`)" \
                     " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (
                         task_id, create_time, device_ip, device_country, device_province, device_city, cpuinfo,
                         longitude, latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def iec104_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='IEC-104')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res, conn=mysql_connect, protocol='IEC-104', timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        testfr_sent_recv = result.get('testfr sent / recv')
        startdt_sent_recv = result.get('startdt sent / recv')
        c_ic_na_1_sent_recv = result.get('c_ic_na_1 sent / recv')
        asdu_address = result.get('asdu address')

        insert_sql = "INSERT INTO `result_iec104`" \
                     "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `testfr_sent_recv`, `startdt_sent_recv`, `c_ic_na_1_sent_recv`, `asdu_address`, `longitude`, `latitude` ,`node_id`, `script_id`, `protocol_id`)" \
                     " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (task_id, create_time, device_ip, device_country, device_province, device_city, testfr_sent_recv,
                        startdt_sent_recv, c_ic_na_1_sent_recv, asdu_address, longitude, latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def http_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='HTTP')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res=res, conn=mysql_connect, protocol="HTTP", timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        device = result.get('device')

        insert_sql = "INSERT INTO `result_http`" \
                     "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `device`, `longitude`, `latitude`, `node_id`, `script_id`, `protocol_id`)" \
                     " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (task_id, create_time, device_ip, device_country, device_province, device_city, device, longitude, latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def moxa_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='MoxaNport')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res=res, conn=mysql_connect, protocol="MoxaNport", timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        vendor = 'moxa'
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        device_status = result.get('device_status')
        server_name = result.get('server_name')

        insert_sql = "INSERT INTO `result_moxa`" \
                     "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `device_status`, `server_name`, `longitude`, `latitude`, `node_id`, `script_id`, `protocol_id`)" \
                     " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor,
                        device_status, server_name, longitude, latitude, node_id, script_id, protocol_id)
        mysql_connect.insert(insert_sql)

def dahua_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id):
    mysql_connect = get_mysql_connect()
    res = NetScan.total_results(dir_path, protocol='Dahua')
    if len(res) == 0:
        return
    res = NetScan.filter_results(res=res, conn=mysql_connect, protocol="Dahua", timestamp=create_time)
    if len(res) == 0:
        return
    for item in res:
        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        device_country = item.get('location').get('country')
        device_province = item.get('location').get('province')
        device_city = item.get('location').get('city')
        result = item.get('result')
        device = result.get('Vendor')
        weakpass = result.get('WeakPass')
        weak = 0 if weakpass is None else 1
        insert_sql ="INSERT INTO `result_dahua`" \
                    "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `device`,`weak_pass`, `longitude`, `latitude`,`node_id`,`script_id`,`protocol_id`)" \
                    " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s','%d', '%s', '%s', '%s', '%s', '%s')" \
                    % (task_id, create_time, device_ip, device_country, device_province, device_city, device,weak, longitude, latitude,node_id,script_id,protocol_id)
        mysql_connect.insert(insert_sql)


def result_to_mysql(dir_path, protocol, create_time, task_id, node_id, script_id, protocol_id):
    print("result to mysql...")
    if protocol == "S7Comm":
        s7comm_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "Modbus":
        modbus_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "EtherNetIP":
        ethernetip_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "Fox":
        fox_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "DNP3":
        dnp3_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "Cspv4":
        cspv4_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "SNMP":
        snmp_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "BACnet":
        bacnet_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "FINS":
        fins_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "MELSEC-Q-TCP":
        melsec_q_tcp_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "MELSEC-Q-UDP":
        melsec_q_udp_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "IEC-104":
        iec104_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "HTTP":
        http_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "MoxaNport":
        moxa_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    elif protocol == "DaHua":
        dahua_to_mysql(dir_path, create_time, task_id, node_id, script_id, protocol_id)
    else:
        print("Wrong Protocol.")
    print("result to mysql done.")

def weak_pass(ip):  # if ip is weak return True
    testURL = 'http://'+ip+'/PSIA/Custom/SelfExt/userCheck'
    headers = {
        'host': ip,
        'Connection': 'keep-alive',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'If-Modified-Since': "0",
        'Authorization': "Basic YWRtaW46MTIzNDU=",  # admin:12345
        'X-Requested-With': "XMLHttpRequest",
        'Referer': "http://101.231.205.106/doc/page/login.asp",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36'}
    try:
        r = requests.get(testURL, headers=headers, timeout=5)
        if re.search('200', r.text):
            return True
    except:  # timeout异常导致慢
        return False

def ip_locate_check():  # 读取文件ip列表，得到每个ip对应的省市，并进行弱口令检测
    with open(r'D:\主动探测\a.json', mode='r+') as f:
        # conn = get_mysql_connect()
        # ip_list, locations = NetScan.get_locations(conn)
        ips = f.read()
        ips = ips.splitlines()
        i = 1
        for ip in ips:
            print(i)
            i += 1
            if weak_pass(ip):
                print(ip)
            # ip_location = locations.get(NetScan.query_target(ip, ip_list))
            # print(ip + ip_location.get('province') + '\t' + ip_location.get('city'))


class Kafka:
    def __init__(self):
        self.mysql_connect = get_mysql_connect()
        print("zooo get mysql connect " + self.mysql_connect.host + ":" + self.mysql_connect.db)

    def fetch_topics(self):
        client = KazooClient()
        client.start()
        @client.DataWatch("/result")
        def watch_task(data, stat, event):
            msg = eval(data.decode())
            if (type(msg) is dict) and (msg.get('msg_type') == 'task_result'):
                print("task get..." + "task_id:" + msg.get('task_id') + " nodeip:" + msg.get('node_ip'))
                task_id = msg.get('task_id')
                node_ip = msg.get('node_ip')
                node_id = self.get_nodeid_by_nodeip(ip=node_ip)
                if node_id == -1:
                    print('Bad node_ip: ' + node_ip)
                if msg.get('task_strategy') is None:
                    print('No task_strategy')
                    return
                task_strategy = msg.get('task_strategy')
                strategy_id = self.get_strategy_id(name=task_strategy)
                if strategy_id == -1:
                    print('Bad task_strategy: ' + task_strategy)
                    return
                task_status = msg.get('task_status')
                if task_status == 'init':
                    task_status = 0
                elif task_status == 'running':
                    task_status = 1
                elif task_status == 'done':
                    task_status = 2
                else:
                    print('Wrong task_status: ' + task_status)
                    return

                update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

                if task_strategy == 'port_scan':
                    try:
                        print("scan type: port_scan")
                        print("updating table: sol_daily.task_detail")
                        self.update_table_task_detail(task_id, node_id, strategy_id, task_status, update_time)
                        print("checking task status...")
                        s = self.check_task_status(task_id=task_id)
                        if s == 2:
                            print("updating table: sol_daily.task")
                            self.update_table_task(task_id=task_id, task_status=s, update_time=update_time)
                    except Exception as e:
                        print(e)
                elif task_strategy == 'protocol_sniffer':
                    try:
                        print("scan type: protocol_sniffer")
                        print("updating table: sol_daily.task_detail")
                        self.update_table_task_detail(task_id, node_id, strategy_id, task_status, update_time)
                        print("checking task status...")
                        s = self.check_task_status(task_id=task_id)
                        if s == 2:
                            print("updating table: sol_daily.task")
                            self.update_table_task(task_id=task_id, task_status=s, update_time=update_time)
                    except Exception as e:
                        print(e)
                    if task_status == 2:  # nmap scan finish, create result file
                        zip_file_name = msg.get('result_name')
                        zip_file_path = r'/opt/net_scan/scan_result'
                        zip_file_name = zip_file_path + '/' + zip_file_name
                        # self.create_zip_file(filename=zip_file_name, task_result=task_result)
                        # print("zip file created...")
                        if not os.path.exists(zip_file_name):
                            print("no zip")
                            return
                        backup_file_path = r'/opt/net_scan/backup/'
                        sys_command1 = 'cp %s %s' % (zip_file_name, backup_file_path)
                        os.popen(sys_command1)
                        print("backup zip file...")

                        xml_file_path = r'/opt/net_scan/scan_result/xml_file'
                        file_list = list()
                        f = zipfile.ZipFile(file=zip_file_name, mode='r')  # extract zip file
                        for file in f.namelist():
                            f.extract(file, xml_file_path)
                            file_list.append(file)
                        f.close()
                        print("zip file extracted...")

                        task_detail = self.get_task_detail(task_id, node_id)
                        if len(task_detail) <= 0:
                            print('Task detail wrong.')
                            return
                        # protocol, create_time, task_id, node_id, script_id, protocol_id
                        create_time = task_detail[0].get('create_time')
                        task_id = task_detail[0].get('task_id')
                        node_id = task_detail[0].get('node_id')
                        script_id = task_detail[0].get('script_id')
                        protocol_id = task_detail[0].get('protocol_id')
                        protocol = self.get_protocol_by_protocolid(protocol_id)

                        #result_to_mysql(xml_file_path, protocol, create_time, task_id, node_id, script_id, protocol_id)

                        xmlfiles = r'/opt/net_scan/scan_result/xml_file/*'
                        sys_command2 = 'rm %s' % xmlfiles
                        #os.popen(sys_command2)
                        print("delete xml files of task_id:" + str(task_id) + ", node_id:" + str(node_id))

                        sys_command3 = 'rm %s' % zip_file_name
                        #os.popen(sys_command3)
                        print("delete " + zip_file_name)

                        print("task done...")

        while True:
            time.sleep(1800)
        client.stop()


    def get_nodeid_by_nodeip(self, ip=None):
        node_sql = "SELECT id,node_ip FROM node"
        res = self.mysql_connect.query(node_sql)
        if res is None:
            return -1
        for node_info in res:
            node_id = node_info.get('id')
            node_ip = node_info.get('node_ip')
            if node_ip == ip:
                return node_id
        return -1

    def get_strategy_id(self, name=None):
        strategy_sql = "SELECT id,strategy_name FROM strategy"
        res = self.mysql_connect.query(strategy_sql)
        for strategy_info in res:
            strategy_id = strategy_info.get('id')
            strategy_name = strategy_info.get('strategy_name')
            if strategy_name == name:
                return strategy_id
        return -1

    def check_task_status(self, task_id):
        check_sql1 = "SELECT COUNT(*) FROM task_detail WHERE task_id='%s' AND task_status='%s'" % (task_id, 2)
        check_sql2 = "SELECT COUNT(*) FROM task_detail WHERE task_id='%s'" % (task_id)
        res1 = self.mysql_connect.query(check_sql1)
        res2 = self.mysql_connect.query(check_sql2)
        if res1 == res2:
            return 2
        else:
            return 1

    def update_table_task(self, task_id, task_status, update_time):
        task_sql = "UPDATE task SET task_status='%s', update_time='%s' WHERE id='%s'" \
                   % (task_status, update_time, task_id)
        self.mysql_connect.insert(task_sql)

    def update_table_task_detail(self, task_id, node_id, strategy_id, task_status, update_time):
        task_detail_sql = "UPDATE task_detail SET strategy_id='%s', task_status='%s', update_time='%s' WHERE task_id='%s' AND node_id='%s'" \
                         % (strategy_id, task_status, update_time, task_id, node_id)
        self.mysql_connect.insert(task_detail_sql)

    def create_zip_file(self, filename, task_result):
        task_result = eval(task_result)
        with open(filename, mode='wb+') as f:
            f.write(task_result)

    def get_task_detail(self, task_id, node_id):
        get_task_detail_sql = "SELECT * FROM task_detail WHERE task_id='%s' AND node_id='%s'" % (task_id, node_id)
        res = self.mysql_connect.query(get_task_detail_sql)
        return res

    def get_protocol_by_protocolid(self, protocolid):
        get_protocol_sql = "SELECT protocol_name FROM protocol WHERE id='%s'" % protocolid
        res = self.mysql_connect.query(get_protocol_sql)
        protocol_name = res[0].get('protocol_name')
        return protocol_name

if __name__ == '__main__':
    k = Kafka()
    k.fetch_topics()
