import xml.etree.cElementTree as ET
import geoip2.database
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


def extract_fingger(scan_file, protocol=None):
    """提取扫描结果文件中的指纹信息

    :Parameters:
      --scan_file：扫描完成后的结果文件

    :Returns:
       dict：key为ip,指纹信息为value
    """

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

    scan_result = []
    try:
        handler = XMLHandler(scan_file)
        host_elements = handler.get_elements(handler.get_root(), "host")
        for host_element in host_elements:
            target_elements = handler.get_elements(host_element, "ports/port/script")
            if target_elements is None or len(target_elements) is 0:
                continue
            address_element = handler.get_element(host_element, "address")
            address = handler.get_attr_value_by_name(address_element, "addr")
            for target_element in target_elements:
                elem_elements = handler.get_elements(target_element, "elem")
                if elem_elements is None or len(elem_elements) is 0:
                    continue
                fingerprint = dict()
                for elem in elem_elements:
                    # 针对特殊协议做参数的格式化
                    if protocol == "FINS":
                        elem_key = handler.get_attr_value_by_name(elem, "key")
                        elem_key = elem_key.replace('.', "") if '.' in elem_key else elem_key
                        if elem_key == 'Controller Model':
                            fingerprint[elem_key] = handler.get_element_value(elem).split(" ")[0]
                        else:
                            fingerprint[elem_key] = handler.get_element_value(elem)
                    elif protocol == "SNMP":
                        elem_key = handler.get_attr_value_by_name(elem, "key")
                        elem_value = handler.get_element_value(elem)
                        if 'Siemens' in elem_value or 'Rockwell' in elem_value or 'Schenider' in elem_value:
                            fingerprint = extract_snmp_figger(handler.get_element_value(elem))
                    else:
                        fingerprint[handler.get_attr_value_by_name(elem, "key")] = handler.get_element_value(elem)
                if len(fingerprint) is 0:
                    pass
                else:
                    scan_item = {"ip": address, "result": fingerprint}
                    scan_result.append(scan_item)
    except:
        pass
    return scan_result


def get_lng_lat(ip):
    """获取给定IP的经纬度"""
    try:
        reader = geoip2.database.Reader(r'D:/tmp/file/GeoLite2-City.mmdb')
        response = reader.city(ip)
        return [response.location.longitude, response.location.latitude,response.location]
    except Exception as e:
        print(e)

if __name__ == "__main__":
    #r = extract_fingger(r'D:\test_e\10.21\res_Enet.xml','EtherNetIP')
    r = get_lng_lat("128.101.101.101")
    print(r)