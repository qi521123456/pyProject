from netscan.__init__ import *
import struct
import os
import socket

class Province:
    #中国省份字典
    PROVINCES = [
       "北京","天津","上海","重庆","河北",
       "河南","云南","辽宁","黑龙江","湖南",
       "安徽","山东","新疆","江苏","浙江",
       "江西","湖北","广西","甘肃","山西",
       "内蒙古","陕西","吉林","福建","贵州",
       "广东","青海","西藏","四川","宁夏",
       "海南","台湾","香港","澳门"
    ]

    @classmethod
    def init_province(cls):
        return { item:{} for item in cls.PROVINCES}


class Analyzer:
    def __init__(self):
        try:
            self.mongo_handler = MongoDBInterface()
            status = self.mongo_handler.connect('localhost', 'SOL', 'admin', 'Free-Wi11')
        except Exception as e:
            print(e)

    def get_protocol_time_point(self):
        """Method for getting the time point of each protocol
        :return:
        """
        try:
            res_list = self.mongo_handler.query("ip,timestamp,parameters","Online",None)
            protocol_list = []
            for line in res_list:
                if line.get("parameters").get("protocol") not in protocol_list :
                    protocol_list.append(line.get("parameters").get("protocol"))
            result = dict()
            for line in protocol_list:
                timestamp_list = []
                res_list = self.mongo_handler.query("ip,timestamp","Online",{"parameters.protocol":line})
                for each in res_list:
                    date = each.get("timestamp")
                    date = date.strftime("%Y-%m-%d")
                    if date not in timestamp_list:
                        timestamp_list.append(date)
                timestamp_list.sort()
                result[line] = timestamp_list
            return result
        except Exception as e:
            return e

    def get_two_timestamp_different(self,protocol,timestamp_pre,timestamp_next):
        """Method for comparing the two timestamp of  appointed protocol

        :param params:"protocol":,"XXXX":,"timestamp1":"2016-04-XX","timestamp2":"XXXX-XX-XX"
        :return:
        """
        try:
            #获取时间点timestamp1
            timestamp1 = timestamp_pre
            timestamp1 = "%s 00:00:00"%timestamp1
            timestamp1 = datetime.datetime.strptime(timestamp1,"%Y-%m-%d %H:%M:%S")
            #获取时间点timestamp2
            timestamp2 = timestamp_next
            timestamp2 = "%s 00:00:00"%timestamp2
            timestamp2 = datetime.datetime.strptime(timestamp2,"%Y-%m-%d %H:%M:%S")
            #pre_ip[]存储时间点1的ip，lat_ip[]存储时间点2的ip
            pre_ip = []
            pre_list = self.mongo_handler.query("ip,result","Online",{"timestamp":timestamp1,"parameters.protocol":protocol})
            for eachline in pre_list:
                pre_ip.append(eachline.get("ip"))

            lat_ip = []
            lat_list = self.mongo_handler.query("ip,result","Online",{"timestamp":timestamp2,"parameters.protocol":protocol})
            for eachline in lat_list:
                lat_ip.append(eachline.get("ip"))
            #over_ip存储时间点2比时间点1多的ip，lack_ip[]存储时间点2比时间点1少的ip
            over_ip = []
            for each in lat_ip:
                if each not in pre_ip:
                    over_ip.append(each)
            lack_ip = []
            for each in pre_ip:
                if each not in lat_ip:
                    lack_ip.append(each)
            #如果over_ip[]和lack_ip[]不为空则返回它们，否则返回指纹信息
            if over_ip or lack_ip:
                temp = {"over_ip":over_ip,"lack_ip":lack_ip,"protocol":protocol,"timestamp_pre":timestamp_pre,"timestamp_next":timestamp_next}
                return temp
            else:
                #attributes存储时间点1的指纹属性，attributes2存储时间点2的指纹属性，over_attributes存储时间点2比时间点1多的属性
                pre = pre_list[0].get("result")
                attributes1 = list(pre.keys())
                late = lat_list[1].get("result")
                attributes2 = list(late.keys())
                over_attributes = []
                for each in attributes2:
                    if each not in attributes1:
                        over_attributes.append(each)
                temp ={"attributes_pre":attributes1,"attributes_next":attributes2,"over_attributes":over_attributes}
                return temp
        except Exception as e:
            return e

    def get_present_ip(self,protocol,timestamp):
        """Method for getting total ip numbel of the appointed protocol by the time point timestamp
        :param params:"protocol":,"timestamp":
        :return:
        """
        try:
            times = timestamp
            times = "%s 00:00:00"%times
            times = datetime.datetime.strptime(times,"%Y-%m-%d %H:%M:%S")
            res_list = self.mongo_handler.query("ip","Online",{"timestamp":{'$lte':times},"parameters.protocol":protocol})
            ip_list = []
            total = 0
            for each in res_list:
                if each.get("ip") not in ip_list:
                    ip_list.append(each.get("ip"))
                    total +=1
            temp = {"protocol":protocol,"timestamp":timestamp,"ip_list":ip_list,"total":total}
            return temp
        except Exception as e:
            return e

    def get_total_ip(self,protocol):
        """Method for getting the total numbel of the appointed protocol
        :param params:{"protocol":}
        :return:
        """
        try:
            res_list = self.mongo_handler.query("ip","Online",{"parameters.protocol":protocol})
            total = 0
            ip_list = []
            for each in res_list:
                if each.get("ip") not in ip_list:
                    ip_list.append(each.get("ip"))
                    total += 1
            temp = {"ip_list":ip_list,"total":total,"protocol":protocol}
            return temp
        except Exception as e:
            return e


class GenerateWord:
    def __init__(self):
        try:
            self.table = {"FINS":['Controller Model','Controller Version'],
                          "IEC-104":['Asdu Address'],
                          "S7COMM":['Version','Module Type'],
                          "EtherNetIP":['Vendor','Product Name'],
                          "ModbusTCP":['Vendor','Device'],
                          "Fox":['Brand ID','Fox Version'],
                          "Dnp3":['Source Address','Control'],
                          "Cspv4":['Session ID'],
                          "FTP":['Device','FTP Server'],
                          "MELSEC-Q":['CPUINFO'],
                          "BACnet":['Application Software']
                          }
            self.mongo_handler = MongoDBInterface()
            status = self.mongo_handler.connect('localhost', 'SOL', 'admin', 'Free-Wi11')
            if status is False:
                print("数据库连接错误")
        except Exception as e:
            return e

    def word(self,protocol,start_time,stop_time,script,db_host='locahost'):
        """

        :param protocol:
        :param vps_node:
        :param start_time:
        :param stop_time:
        :param script:
        :return:
        """
        try:
            #判断文件是否存在，如果存在改为追加内容
            """filename = 'D:\demo.docx'
            if os.path.exists(filename):
                document = Document('D:\demo.docx')
            else:
                document = Document()
                heading = document.add_heading()
                heading.add_run('结果分析', 0)
                document.add_heading('结果详细', 2)
            #协议的基本信息
            document.add_heading('%s'%protocol,3)
            str1 = "1 VPS:%s \n2 扫描开始时间：%s\n3 扫描结束时间:%s\n4 扫描方式：端口识别+脚本扫描\n5 " \
                   "脚本：%s\n6 详细信息:"%(db_host,start_time,stop_time,script)
            document.add_paragraph(str1)

            #查询数据库找出总共的条数
            timestamp1 = "%s 00:00:00" % start_time
            timestamp1 = datetime.datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S")
            timestamp2 = "%s 00:00:00" % stop_time
            timestamp2 = datetime.datetime.strptime(timestamp2, "%Y-%m-%d %H:%M:%S")
            res_list = self.mongo_handler.query(None, "Online", {"parameters.protocol": protocol,'timestamp':{'$gte':timestamp1,'$lte':timestamp2}})

            #根据属性类追加内容
            attributes = self.table[protocol]
            cols_len = len(attributes) + 2
            #表头
            table = document.add_table(rows=1,cols=cols_len)
            table.style = 'Table Grid'
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = 'IP'
            hdr_cells[1].text = 'Location'
            if len(attributes) is not 0:
                hdr_cells[2].text = attributes[0]
                hdr_cells[3].text = attributes[1]

            #添加表的内容
            for eachline in res_list:
                row_cells = table.add_row().cells
                row_cells[0].text = eachline.get("ip")
                row_cells[1].text = eachline.get("location")
                i = 2
                for each in attributes:
                    if eachline.get("result").get(each) is not None:
                        row_cells[i].text = eachline.get("result").get(each)
                    i += 1
            row_cells = table.add_row().cells
            row_cells[0].text = "总计"
            row_cells[1].text = str(len(res_list))

            document.save('D:\demo.docx')"""
            pass
        except Exception as e:
            return e


class IPCompare:
    def __init__(self):
        try:
            self.mongo_handler = MongoDBInterface()
            self.ip_handler = Analyzer()
            status = self.mongo_handler.connect('localhost', 'SOL', 'admin', 'Free-Wi11')
            if status is False:
                print("数据库连接错误")
        except Exception as e:
            return e

    def generate_ipcompare_result(self,protocol,timestamp_pre='NULL',timestamp_next='NULL',db_node='localhost'):
        """

        :param protocol:
        :param timestamp_pre:
        :param timestamp_next:
        :param db_node:
        :return:
        """
        try:
            filename = 'D:\ipcompare.docx'
            if os.path.exists(filename):
                document = Document('D:\ipcompare.docx')
            else:
                document = Document()

            #如果没有输入日期，则默认为最新的两次
            if timestamp_pre is 'NULL' and timestamp_next is 'NULL':
                res = self.ip_handler.get_protocol_time_point()
                time_list = res[protocol]
                timestamp_next = time_list[-1]
                timestamp_pre = time_list[-2]

            #加入标头信息
            str1 = "1 扫描开始时间：%s\n2 扫描结束时间:%s\n3 详细信息:"%(timestamp_pre,timestamp_next)
            document.add_heading('%s' % protocol, 3)
            document.add_paragraph(str1)

            #生成ip的对比结果
            res = self.ip_handler.get_two_timestamp_different(protocol,timestamp_pre,timestamp_next)

            over_ip = []
            lack_ip = []
            finger = []

            if res.get("over_ip") and res.get("lack_ip"):
                over_ip = res.get("over_ip")
                lack_ip = res.get("lack_ip")
                table = document.add_table(rows=1, cols=2)
                table.style = 'Table Grid'
                hdr_cells = table.rows[0].cells
                hdr_cells[0].text = '新增IP'
                hdr_cells[1].text = '缺失IP'
                temp = 0

                while temp < len(over_ip) or temp < len(lack_ip):
                    row_cells = table.add_row().cells
                    if temp <len(over_ip):
                        row_cells[0].text = over_ip[temp]
                    if temp < len(lack_ip):
                        row_cells[1].text = lack_ip[temp]
                    temp += 1
                row_cells = table.add_row().cells
                row_cells[0].text = str(len(over_ip))
                row_cells[1].text = str(len(lack_ip))
            elif res.get("over_attributes"):
                table = document.add_table(rows=1, cols=1)
                table.style = 'Table Grid'
                hdr_cells = table.rows[0].cells
                hdr_cells[0].text = '增加的指纹'
                finger = res.get("over_attributes")
                for each in finger:
                    row_cells = table.add_row().cells
                    row_cells[0].text = each
            else:
                print("Error")
            document.save('D:\ipcompare.docx')
        except Exception as e:
            return e


class FlowAnalyzer:

    def file_iterator(self,file_name,seperator):
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

    def save_file(self,file_name,data_source):
        if type(data_source) is not list:
            print("data source invalid")
        else:
            with open(file_name,'w+',encoding='UTF-8') as fp:
                for data in data_source:
                    fp.write(data+"\n")

    def extract_snmp_figger2(self,device_info):
        device_figger = dict()
        try:
            if 'Siemens' in device_info:
                figger_items = device_info.split(',')
                for f_item in figger_items:
                    if 'Siemens' in f_item:
                        device_figger['Vendor'] = 'Siemens'
                        continue
                    if 'SIMATIC' in f_item:
                        device_figger['System Name'] = f_item.strip()
                        continue
                    if 'CPU' in f_item or 'CP' in f_item:
                        device_figger['Module Type'] = f_item.strip()
                        continue
                    if '6ES7' in f_item or '6GK7' in f_item:
                        device_figger['Basic Hardware'] = f_item.strip()
                        continue
                    if 'HW' in f_item:
                        hw_info = f_item.split(':')
                        device_figger['HW'] = hw_info[1].strip()
                        continue
                    if 'FW' in f_item:
                        fw_info = f_item.split(':')
                        device_figger['FW'] = fw_info[1].strip()
                        continue
                if figger_items[len(figger_items)-1] not in device_figger.items():
                    device_figger['Serial Number'] = figger_items[len(figger_items)-1].strip()
            elif 'Rockwell' in device_info:
                pass
            elif 'Schenider' in device_info:
                pass
        except:
            pass
        finally:
            return device_figger

    def extract_snmp_figger(self,device_info):
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
    def extract_ip(self,src_file):
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

#-----------------------------------------------------------------------

class NetScan:
    """空间设备扫描的工具类，封装了自动化设计的工具方法"""
    Logger = Logging().get_logger()

    @classmethod
    def get_ip_list(cls,file):
        """从指定文件里返回IP地址列表
        :Parameters:
           --file：源文件路径

        :Returns:
           ip_list：ip地址列表
        """
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
    def split_file(cls,file,prefix,file_number=5,extension="txt",parent=None):
        """分割大文件成制定个数的小文件
        :Parameters:
            --file: 待分割源文件
            --prefix: 目标文件前缀名
            --file_number：被分割目标文件数
            --extension：目标文件扩展名,默认为txt
        """
        def create_file(new_file_name,datas):
            """创建新文件
            :Parameters:
               --new_file_name：目标文件名
               datas：写入文件的数据,类型为list
            """
            if type(datas) != list:
                cls.Logger.warning("Data type invalid")
            else:
                with open(parent+"\\"+new_file_name,"w+",encoding='UTF-8') as f:
                    for data in datas:
                        f.write(data+"\n")

        try:
            file_opener= open(file,encoding="UTF-8")
        except FileNotFoundError:
            cls.Logger.error("File not found")
        else:
            ip_list = cls.get_ip_list(file)
            if len(ip_list) is 0:
                cls.Logger.warning("IP list is empty")
            else:
                single_size = len(ip_list) // file_number
                index ,current,total = 1, 0, 0
                while index <= file_number:
                    total = current + single_size
                    sub_list = ip_list[current:total] if index < file_number else ip_list[current:]
                    file_name = "%s_%s.%s" % (prefix,str(index),extension)
                    create_file(file_name,sub_list)
                    index+=1
                    current+=single_size
        cls.Logger.info("Split File Finish.")

    @classmethod
    def get_area(cls,ip_address):
        """获取给定IP的地理位置
        :Paprameters:
           -ip_address：合法的ip地址
        """
        def extract(content):
            """从网页内容中提取地理位置
            :Parameters:
              --content：过滤后的网页内容
            """
            try:
                return content[content.find("：")+1:len(content)].split(" ")[0]
            except:
                NetScan.Logger.warning("No area by given address")
                return "China"
        try:
            query = requests.get("http://www.ip138.com/ips138.asp",{"ip":ip_address})
            result = BeautifulSoup(query.content).find("ul",{"class":"ul1"})
            return extract(result.find("li").text)
        except:
            cls.Logger.warning("Network error,please check.")
            return "China"

    @classmethod
    def get_area_api(cls, ip_address):
        """利用百度地图api获取给定ip的地理位置

        :param ip_address: 合法的ip地址
        :return:
        """
        url = "http://api.map.baidu.com/location/ip"
        payload = {"ip": ip_address, "ak": "hBVLinbYjQN3PpWmKp88xckDUTinAhas"}
        try:
            res = requests.get(url=url, params=payload).text
            res = json.loads(res)
            if res.get("status") is 0:
                area = res.get("content").get("address")
            else:
                area = "国外"
            return area
        except Exception as e:
            cls.Logger.error(e)

    @classmethod
    def get_lng_lat_bd(cls, area):
        """获取给定地理位置的经纬度

        :param area: 合法的地理位置,例如"浙江省衢州市"
        :return: {"lng": "118.875841652", "lat": "28.9569104475"}
        """
        url = "http://api.map.baidu.com/geocoder/v2/"
        payload = {"address": area, "ak": "hBVLinbYjQN3PpWmKp88xckDUTinAhas", "output": "json"}
        try:
            res = requests.get(url=url, params=payload).text
            res = json.loads(res)
            result = res.get("result").get("location")
            return [result.get('lng'),result.get('lat')]
        except Exception as e:
            cls.Logger.error(e)

    @classmethod
    def get_lng_lat(cls, ip):
        """获取给定IP的经纬度"""
        try:
            reader = geoip2.database.Reader(r'file/GeoLite2-City.mmdb')
            response = reader.city(ip)
            return [response.location.longitude,response.location.latitude]
        except Exception as e:
            cls.Logger.error(e)

    @classmethod
    def sort_target(cls,target_file):
        """按照地理位置分类目标IP
          :Parameters:
            --target_file：包含目标IP的文件
          :Returns:
            dict：key为province,value为ip
        """

        def check(pre_sort,after_sort):
            """校验分类后的结果是否有遗漏的IP
            :Parameters:
              --pre_sort：分类前的IP列表
              --after_sort：分类后的IP省份字典
            """
            counter = 0
            for item in after_sort:
                counter += len(after_sort.get(item))
            return counter == len(pre_sort)

        provinces = Province.init_province()
        ip_list = cls.get_ip_list(target_file)
        for ip in ip_list:
            ip_area = cls.get_area(ip)
            for province in provinces:
                if province in ip_area:
                    if provinces[province].get(ip_area) is None:
                        provinces[province][ip_area] = list()
                    provinces[province][ip_area].append(ip)
                    break
        soretd_targets = {}
        for province in provinces:
            if len(provinces.get(province)) > 0:
                soretd_targets[province] = provinces.get(province)

        if not check(ip_list,soretd_targets):
            cls.Logger.warning("Maybe some ip ignored")
        return soretd_targets

    @classmethod
    def extract_fingger(cls,scan_file,protocol=None):
        """提取扫描结果文件中的指纹信息

        :Parameters:
          --scan_file：扫描完成后的结果文件

        :Returns:
           dict：key为ip,指纹信息为value
        """
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
                        #针对特殊协议做参数的格式化
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
    def echo_targets(cls,d_targets):
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
    def total_results(cls,dir_path,protocol=None,extension="xml"):
        """统计给定目录下指定格式的结果"""
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
    def filter_results(cls,results,conn=None,**attach):
        """将结果过滤，只保存国内的结果

        :param results: results from total_results method
        :param attach:
        :return: filtered results
        """
        filter_results = []
        try:
            for result in results:
                #area = cls.get_area(result.get("ip"))
                area = get_location(result.get("ip"),conn)
                if area == "Unknown":
                    continue
                #area = cls.get_area_api(result.get("ip"))
                for country in Province.PROVINCES:
                    if country in area:
                        lng_lat = cls.get_lng_lat(result.get('ip'))
                        result["geo"] = lng_lat
                        result["location"] = area
                        if attach.get("protocol") is not None:
                            result["protocol"] = attach.get("protocol")
                        if attach.get("timestamp") is not None:
                            result["timestamp"] = datetime.datetime.strptime(attach.get("timestamp"), "%Y-%m-%d")
                        filter_results.append(result)
                        break
        except:
            cls.Logger.warning("May be problem happned")
        return filter_results

def get_connect(ip=None):
    mi = MongoDBInterface()
    if ip is None:
        mi.connect('127.0.0.1','SOL','admin','Free-Wi11')
    else:
        mi.connect(ip,'SOL','admin','Free-Wi11')
    return mi


def get_mysql_connect(ip=None, db='test'):  # add by lhb
	if ip is None:
		conn = MysqlInterface(host="localhost", user="root", password="123456", db=db)
	else:
		conn = MysqlInterface(host=ip, user="root", password="123456", db=db)
	return conn


def query(**kwargs):
    connect = get_connect()
    if kwargs.get('timestamp') is not None:
        timestamp = datetime.datetime.strptime(kwargs.get('timestamp'),"%Y-%m-%d")
    if kwargs.get("protocol") is not None:
        protocol = kwargs.get('protocol')
    result = connect.query(None,'Online',{'timestamp':timestamp,'parameters.protocol':protocol})
    connect.disconnect()
    return result

def save(results):
    handler = MongoDBInterface()
    handler.connect('127.0.0.1','SOL','admin','Free-Wi11')
    for result in results:
        handler.insert(result,'Online',None)
    handler.disconnect()

def get_date(date_str):
    return datetime.datetime.strptime(date_str,"%Y-%m-%d")
#BACnet:     7-20
#EtherNetIP: 7-23
#FINS-TCP :  7-23
#IEC-104  :  7-23
#Modbus   :  7-25
#S7Comm   :  7-20
#SNMP     :  7-25
#DNP3     :  7-30
#Fox      :  7-30
#FINS-UDP :  7-30
#Cspv4: 7-31
#FTP : 7-18
#Codesys 8-10 No Result
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
    return  open_ip_list

def get_30():
    d = dict()
    file = open('30/30-data.txt')
    line = file.readline()
    while True:
        if not line:
            break
        line = line.split('\t')
        d[line[0]] = line[3]
        line = file.readline()
    file.close()
    return d

def get_target(start_ip,end_ip):
    if start_ip == end_ip:
        return start_ip
    s_ip = start_ip.split('.')
    e_ip = end_ip.split('.')
    for i in range(len(s_ip)):
        if s_ip[i] != e_ip[i]:
            scope = (i+1) * 8
            result = start_ip+"/%s" % str(scope)
            return result

def get_src(pcap_file):
    from pcapfile import savefile
    testcap = open(pcap_file,'rb')
    capfile = savefile.load_savefile(testcap, layers=2, verbose=True)
    s = set()
    for packet in capfile.packets:
        ip = packet.packet.payload.src.decode()
        s.add(ip)
    return s

def get_location(target_ip,conn):
    location = None
    try:
        target_ip = socket.ntohl(struct.unpack("I",socket.inet_aton(target_ip))[0])
        query_res = conn.query(None,'ipChina',{'start_ip':{'$lte':target_ip},'end_ip':{'$gte':target_ip}})
        if len(query_res) is 0:
            location = 'Unknown'
        else:
            location = query_res[0].get('location')
    except Exception as ex:
        print(ex)
        location = 'Unknown'
    finally:
        return location


def get_siemens(query_start,query_end):
    query_start = datetime.datetime.strptime(query_start,"%Y-%m-%d")
    query_end = datetime.datetime.strptime(query_end,"%Y-%m-%d")
    conn = get_connect()
    result = {
        'SNMP':[],
        'S7Comm':[],
        'Modbus':[],
        'EtherNetIP':[]
    }
    for protocol in result.keys():
        res = conn.query(None,'Online',{'protocol':protocol,'timestamp':{"$gte":query_start,"$lte":query_end}})
        for record in res:
            if protocol == 'S7Comm':
                result[protocol].append(record)
            else:
                if 'Siemens' in str(record.get('result')):
                    result[protocol].append(record)
    ips = list()
    for key in result.keys():
        for item in result[key]:
            if item.get('ip') in ips:
                result[key].remove(item)
            else:
                ips.append(item.get('ip'))
    return result

class Siemens:
    IP = None
    LOCATION = None
    PROTOCOL = None
    VENDOR = "Siemens"
    BRAND = None
    CPU = None
    FW = None
    HW = None
    ORDER = None
    SERAIL = None

def analysis(a_targets):
    result = dict()
    for record in a_targets:
        items = record.split("\t")
        p = items[1][:2]
        if result.get(p) is None:
            result[p] = list()
        result[p].append(record)

    print(len(result.keys()))
    return result

PROVINCE_GROUP = [
    "北京","山东","台湾","黑龙江","上海","广东","吉林",
    "浙江","辽宁","江苏","新疆","广西","山西","江西",
    "湖南","湖北","河南","河北","云南","西藏","内蒙",
    "陕西","甘肃","宁夏","重庆","青海","天津","四川",
    "香港","澳门","福建","安徽","贵州","海南"
]

def simenes_report():
    records = get_siemens('2016-11-01','2016-11-30')
    targets = list()
    for protocol in records.keys():
        result = records[protocol]
        for item in result:
            #print(str(item.get('result')))
            Siemens.IP = item.get('ip')
            Siemens.LOCATION = item.get('location')
            if protocol == 'Modbus':
                Siemens.BRAND = item.get('result').get('Device')
                Siemens.CPU = item.get('result').get('Revision')
            else:
                if item.get('result').get('figger') is not None:
                    #print(item)
                    temp_result = FlowAnalyzer().extract_snmp_figger2(item.get('result').get('figger'))
                else:
                    temp_result = item.get('result')
                Siemens.BRAND = temp_result.get('System Name')
                Siemens.CPU = temp_result.get('Module Type')
                Siemens.FW = temp_result.get('FW')
                Siemens.HW = temp_result.get('HW')
                Siemens.ORDER = temp_result.get('Basic Hardware')
                Siemens.SERAIL = temp_result.get('Serial Number')
            temp = str(Siemens.IP) + "\t"+Siemens.LOCATION+"\t"+ str(Siemens.BRAND )+"\t" + str(Siemens.CPU)+"\t"+str(Siemens.FW)+"\t"+ \
                   str(Siemens.HW) + "\t" + str(Siemens.ORDER)+"\t" + str(Siemens.SERAIL)

            targets.append(temp)

    new_targets = analysis(targets)
    ips = list()
    for province in PROVINCE_GROUP:
        values = new_targets.get(province)
        if values is not None and len(values) > 0:
            for v in values:
                ip = v.split('\t')[0]
                if ip not in ips:
                    ips.append(ip)
                    print(v)

def weak_pass(ip):
    # 测试单个ip
    testURL = 'http://'+ip+'/PSIA/Custom/SelfExt/userCheck'
    headers = {
        'host': ip,
        'Connection': 'keep-alive',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'If-Modified-Since': "0",
        'Authorization': "Basic YWRtaW46MTIzNDU=",#admin:12345
        'X-Requested-With': "XMLHttpRequest",
        'Referer': "http://101.231.205.106/doc/page/login.asp",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2859.0 Safari/537.36'}
    #s = requests.session()
    try:
        r = requests.get(testURL,headers=headers,timeout=5)
        #print(r.text)
        if re.search('200',r.text):
            return True
    except:#timeout异常导致慢
        return False

def get_device_by_sn(date=None):
    query_res = dict()
    query_condition = None
    if date is not None:
        query_condition = {'timestamp':{'$gte':datetime.datetime.strptime(date,"%Y-%m-%d")}}
    mi = get_connect('10.0.1.188')
    result = mi.query(None,'Online',query_condition)
    for q_item in result:
        device_info = q_item.get('result')
        if device_info.get('Serial Number') is not None:
            sn = device_info.get('Serial Number').strip()
            if sn[0] == 'S':
                if query_res.get(sn) is None:
                    query_res[sn] = list()
                    query_res[sn].append(q_item.get('ip'))
                else:
                    if q_item.get('ip') not in query_res[sn]:
                        query_res[sn].append(q_item.get('ip'))
    return query_res

class siemens:
    def __init__(self):
        self.ip = None
        self.location = None
        self.protocol = None
        self.vendor = None
        self.brand = None
        self.cpu = None
        self.fw = None
        self.hw = None
        self.order = None
        self.serail = None


def result_to_mongodb():  # add by lhb
	conn1 = get_connect('127.0.0.1')
	conn2 = get_connect('10.0.1.188')
	res = NetScan.total_results('D:\Res\Res', protocol='HTTP')
	res = NetScan.filter_results(res, conn=conn1, protocol='HTTP', timestamp='2016-12-21')
	num = 0
	for item in res:
		print(item)
		conn1.insert(item, 'Online', None)
		conn2.insert(item, 'Online', None)
		num += 1
	print(num)


def get_result_from_mongodb():  # add by lhb
	conn1 = get_connect('10.0.1.188')
	q_datetime = datetime.datetime.strptime('2016-12-21', '%Y-%m-%d')
	res = conn1.query(None, 'Online', {'timestamp': q_datetime, 'protocol': 'IEC-104'})
	num = 0
	for item in res:
		# if '黑龙江' in item.get('location'):
		# 	ip = item.get('ip')
		# 	if weak_pass(ip):
		# 		print(item)
		# 		num += 1
		if '黑龙江' in item.get('location'):
			num += 1
			print(item)
			# print(item.get('ip') + '\t' + item.get('location').split()[0] + '\t' + '西门子' + '\t' + 'SNMP' + '\t' + item.get('result').get('figger'))
	print(num)


def get_result_from_mysql(table_name, create_time):
	mongo_conn = get_connect('127.0.0.1')
	conn = get_mysql_connect(ip='10.0.1.188', db='sol')
	sql = "SELECT * FROM %s WHERE create_time='%s'" % (table_name, create_time)
	res = conn.query(sql)
	num = 0
	for item in res:
		if '澳门' in item.get('device_province'):
			if weak_pass(item.get('device_ip')):
				print(item.get('device_ip') + '\t' + item.get('device_province'))
				num += 1
	print(num)


def mongodb_to_mysql_S7Comm():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	# q_datetime = datetime.datetime.strptime("2016-12-14", "%Y-%m-%d")
	res = mongo_connect.query(None, "Online", {'protocol': 'S7Comm'})
	# res = mongo_connect.query(None, "Online", None)
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\time.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['timestamp'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		basic_hardware = result.get('Basic Hardware')
		system_name = result.get('System Name')
		module_type = result.get('Module Type')
		module = result.get('Module')
		version = result.get('Version')
		serial_number = result.get('Serial Number')
		copyright = result.get('Copyright')

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		vendor = 'Siemens'
		insert_sql = "INSERT INTO `result_s7comm`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `basic_hardware`, `system_name`, `module_type`, `module`, `version`, `serial_number`, `copyright`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor, basic_hardware, system_name, module_type, module, version, serial_number, copyright, longitude, latitude)
		# print(insert_sql)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def mongodb_to_mysql_Modbus():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	# q_datetime = datetime.datetime.strptime("2016-12-14", "%Y-%m-%d")
	res = mongo_connect.query(None, "Online", {'protocol': 'Modbus'})
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\modbus_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		vendor = result.get('Vendor')
		revision = result.get('Revision')
		device = result.get('Device')
		if vendor == 'Siemens':  # 特殊判断
			if revision is not None:
				device = device + ' ' + revision
				revision = None


		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_modbus`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `revision`, `device`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor, revision, device,  longitude, latitude)
		# print(insert_sql)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def mongodb_to_mysql_EtherNetIP():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	# q_datetime = datetime.datetime.strptime("2016-12-14", "%Y-%m-%d")
	res = mongo_connect.query(None, "Online", {'protocol': 'EtherNetIP'})
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\modbus_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		vendor = result.get('Vendor')
		product_name = result.get('Product Name')
		serial_number = result.get('Serial Number')
		device_type = result.get('Device Type')
		product_code = result.get('Product Code')
		revision = result.get('Revision')


		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_ethernetip`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `product_name`, `serial_number`, `device_type`, `product_code`, `revision`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor, product_name, serial_number,  device_type, product_code, revision, longitude, latitude)
		# print(insert_sql)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def mongodb_to_mysql_Fox():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	# q_datetime = datetime.datetime.strptime("2016-12-14", "%Y-%m-%d")
	res = mongo_connect.query(None, "Online", {'protocol': 'Fox'})
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\fox_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item, ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
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


		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_fox`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `fox_version`, `host_name`, `application_name`, `application_version`, `vm_name`, `vm_version`, `os_name`, `time_zone`, `host_id`, `vm_uuid`, `brand_id`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, fox_version, host_name, application_name,  application_version, vm_name, vm_version, os_name, time_zone, host_id, vm_uuid, brand_id, longitude, latitude)
		# print(insert_sql)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def mongodb_to_mysql_DNP3():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	# q_datetime = datetime.datetime.strptime("2016-12-14", "%Y-%m-%d")
	res = mongo_connect.query(None, "Online", {'protocol': 'DNP3'})
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\dnp3_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		destination_address = result.get('Destination Address')
		source_address = result.get('Source Address')
		control = result.get('Control')

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_dnp3`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `destination_address`, `source_address`, `control`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, destination_address, source_address, control, longitude, latitude)
		# print(insert_sql)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def mongodb_to_mysql_Cspv4():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	# q_datetime = datetime.datetime.strptime("2016-12-14", "%Y-%m-%d")
	res = mongo_connect.query(None, "Online", {'protocol': 'Cspv4'})
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\dnp3_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		session_id = result.get('Session ID')

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_cspv4`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `session_id`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, session_id, longitude, latitude)
		# print(insert_sql)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def mongodb_to_mysql_BACnet():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	# q_datetime = datetime.datetime.strptime("2016-12-14", "%Y-%m-%d")
	res = mongo_connect.query(None, "Online", {'protocol': 'BACnet'})
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\bacnet_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue

		# result = item.get('result')  # mongodb里部分bacnet协议有错，将其protocol字段修改为SNMP
		# figger = result.get('figger')
		# if figger is not None:
		# 	tid = item.get('_id')
		# 	mongo_connect.update({'protocol': 'SNMP'}, 'Online', {'_id': tid})
		# 	num += 1
		# 	print(num)

		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
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

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_bacnet`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor_id`, `vendor_name`, `instance_number`, `firmware`, `application_software`, `object_name`, `object_identifier`, `model_name`, `description`, `location`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor_id, vendor_name, instance_number, firmware, application_software, object_name, object_identifier, model_name, description, location, longitude, latitude)
		# print(insert_sql)
		if num == 88:  # 特殊字符处理
			insert_sql = "INSERT INTO `result_bacnet`(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor_id`, `vendor_name`, `instance_number`, `firmware`, `application_software`, `object_name`, `object_identifier`, `model_name`, `description`, `location`, `longitude`, `latitude`) VALUES ('37', '2016-10-21 00:00:00', '61.183.8.38', '中国', '湖北', '武汉', 'Siemens Schweiz AG (Formerly: Landis & Staefa Division Europe) (7)', 'Siemens Building Technologies', 'None', 'FW=V4.00.060 / SBC=05.10 / FLI=04.00 / BBI=10.05 / STF=01.10', 'Appl_SW_Vers', 'Hovari1 AS01', '2100225', 'PXC100ED / HW=V1.00', 'PXC Contr. 01. YouYi Building', 'None', '114.2734', '30.5801')"
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def mongodb_to_mysql_FINS():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	# q_datetime = datetime.datetime.strptime("2016-12-14", "%Y-%m-%d")
	res = mongo_connect.query(None, "Online", {'protocol': 'FINS'})
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\fins_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue

		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
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

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_fins`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `controller_model`, `controller_version`, `for_system_use`, `program_area_size`, `iom_size`, `no_dm_words`, `timer_counter`, `expansion_dm_size`, `no_of_steps_transitions`, `kind_of_memory_card`, `memory_card_size`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, controller_model, controller_version, for_system_use, program_area_size, iom_size, no_dm_words, timer_counter, expansion_dm_size, no_of_steps_transitions, kind_of_memory_card, memory_card_size, longitude, latitude)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def mongodb_to_mysql_IEC104():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	# q_datetime = datetime.datetime.strptime("2016-12-14", "%Y-%m-%d")
	res = mongo_connect.query(None, "Online", {'protocol': 'IEC-104'})
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\iec104_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue

		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		testfr_sent_recv = result.get('testfr sent / recv')
		startdt_sent_recv = result.get('startdt sent / recv')
		c_ic_na_1_sent_recv = result.get('c_ic_na_1 sent / recv')
		asdu_address = result.get('asdu address')

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_iec104`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `testfr_sent_recv`, `startdt_sent_recv`, `c_ic_na_1_sent_recv`, `asdu_address`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, testfr_sent_recv, startdt_sent_recv, c_ic_na_1_sent_recv, asdu_address, longitude, latitude)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def mongodb_to_mysql_HTTP():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	# q_datetime = datetime.datetime.strptime("2016-12-14", "%Y-%m-%d")
	res = mongo_connect.query(None, "Online", {'protocol': 'HTTP'})
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\http.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue

		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		device = result.get('device')

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_http`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `device`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, device, longitude, latitude)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def mongodb_to_mysql_SNMP():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	# q_datetime = datetime.datetime.strptime("2016-12-14", "%Y-%m-%d")
	res = mongo_connect.query(None, "Online", {'protocol': 'SNMP'})
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\snmp.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)
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
				print('stop')
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
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `brand`, `cpu`, `fireware_version`, `hardware_version`, `order_no`, `serial_number`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor, brand, cpu, fireware_version, hardware_version, order_no, serial_number, longitude, latitude)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def get_taskid_by_createtime(create_time):
	if (create_time == datetime.datetime.strptime('2016-04-22', '%Y-%m-%d')):
		task_id = 1
	elif (create_time == datetime.datetime.strptime('2016-04-25', '%Y-%m-%d')):
		task_id = 2
	elif (create_time == datetime.datetime.strptime('2016-04-26', '%Y-%m-%d')):
		task_id = 3
	elif (create_time == datetime.datetime.strptime('2016-04-27', '%Y-%m-%d')):
		task_id = 4
	elif (create_time == datetime.datetime.strptime('2016-04-29', '%Y-%m-%d')):
		task_id = 5
	elif (create_time == datetime.datetime.strptime('2016-05-04', '%Y-%m-%d')):
		task_id = 6
	elif (create_time == datetime.datetime.strptime('2016-05-06', '%Y-%m-%d')):
		task_id = 7
	elif (create_time == datetime.datetime.strptime('2016-05-10', '%Y-%m-%d')):
		task_id = 8
	elif (create_time == datetime.datetime.strptime('2016-05-11', '%Y-%m-%d')):
		task_id = 9
	elif (create_time == datetime.datetime.strptime('2016-05-14', '%Y-%m-%d')):
		task_id = 10
	elif (create_time == datetime.datetime.strptime('2016-05-16', '%Y-%m-%d')):
		task_id = 11
	elif (create_time == datetime.datetime.strptime('2016-05-17', '%Y-%m-%d')):
		task_id = 12
	elif (create_time == datetime.datetime.strptime('2016-05-19', '%Y-%m-%d')):
		task_id = 13
	elif (create_time == datetime.datetime.strptime('2016-05-20', '%Y-%m-%d')):
		task_id = 14
	elif (create_time == datetime.datetime.strptime('2016-05-24', '%Y-%m-%d')):
		task_id = 15
	elif (create_time == datetime.datetime.strptime('2016-05-26', '%Y-%m-%d')):
		task_id = 16
	elif (create_time == datetime.datetime.strptime('2016-06-02', '%Y-%m-%d')):
		task_id = 17
	elif (create_time == datetime.datetime.strptime('2016-06-06', '%Y-%m-%d')):
		task_id = 18
	elif (create_time == datetime.datetime.strptime('2016-06-08', '%Y-%m-%d')):
		task_id = 19
	elif (create_time == datetime.datetime.strptime('2016-06-09', '%Y-%m-%d')):
		task_id = 20
	elif (create_time == datetime.datetime.strptime('2016-06-20', '%Y-%m-%d')):
		task_id = 21
	elif (create_time == datetime.datetime.strptime('2016-06-27', '%Y-%m-%d')):
		task_id = 22
	elif (create_time == datetime.datetime.strptime('2016-06-30', '%Y-%m-%d')):
		task_id = 23
	elif (create_time == datetime.datetime.strptime('2016-07-20', '%Y-%m-%d')):
		task_id = 24
	elif (create_time == datetime.datetime.strptime('2016-07-23', '%Y-%m-%d')):
		task_id = 25
	elif (create_time == datetime.datetime.strptime('2016-07-25', '%Y-%m-%d')):
		task_id = 26
	elif (create_time == datetime.datetime.strptime('2016-07-28', '%Y-%m-%d')):
		task_id = 27
	elif (create_time == datetime.datetime.strptime('2016-07-30', '%Y-%m-%d')):
		task_id = 28
	elif (create_time == datetime.datetime.strptime('2016-07-31', '%Y-%m-%d')):
		task_id = 29
	elif (create_time == datetime.datetime.strptime('2016-08-20', '%Y-%m-%d')):
		task_id = 30
	elif (create_time == datetime.datetime.strptime('2016-09-18', '%Y-%m-%d')):
		task_id = 31
	elif (create_time == datetime.datetime.strptime('2016-09-20', '%Y-%m-%d')):
		task_id = 32
	elif (create_time == datetime.datetime.strptime('2016-09-28', '%Y-%m-%d')):
		task_id = 33
	elif (create_time == datetime.datetime.strptime('2016-09-30', '%Y-%m-%d')):
		task_id = 34
	elif (create_time == datetime.datetime.strptime('2016-10-08', '%Y-%m-%d')):
		task_id = 35
	elif (create_time == datetime.datetime.strptime('2016-10-17', '%Y-%m-%d')):
		task_id = 36
	elif (create_time == datetime.datetime.strptime('2016-10-21', '%Y-%m-%d')):
		task_id = 37
	elif (create_time == datetime.datetime.strptime('2016-11-01', '%Y-%m-%d')):
		task_id = 38
	elif (create_time == datetime.datetime.strptime('2016-11-02', '%Y-%m-%d')):
		task_id = 39
	elif (create_time == datetime.datetime.strptime('2016-11-17', '%Y-%m-%d')):
		task_id = 40
	elif (create_time == datetime.datetime.strptime('2016-11-20', '%Y-%m-%d')):
		task_id = 41
	elif (create_time == datetime.datetime.strptime('2016-11-21', '%Y-%m-%d')):
		task_id = 42
	elif (create_time == datetime.datetime.strptime('2016-11-30', '%Y-%m-%d')):
		task_id = 43
	elif (create_time == datetime.datetime.strptime('2016-12-07', '%Y-%m-%d')):
		task_id = 44
	elif (create_time == datetime.datetime.strptime('2016-12-14', '%Y-%m-%d')):
		task_id = 45
	elif (create_time == datetime.datetime.strptime('2016-12-21', '%Y-%m-%d')):
		task_id = 46
	elif (create_time == datetime.datetime.strptime('2016-12-20', '%Y-%m-%d')):
		task_id = 47
	elif (create_time == datetime.datetime.strptime('2016-12-28', '%Y-%m-%d')):
		task_id = 48
	elif (create_time == datetime.datetime.strptime('2017-01-04', '%Y-%m-%d')):
		task_id = 49
	elif (create_time == datetime.datetime.strptime('2017-01-11', '%Y-%m-%d')):
		task_id = 50
	elif (create_time == datetime.datetime.strptime('2017-01-18', '%Y-%m-%d')):
		task_id = 51
	return task_id


def tables_compare():  # add by lhb
	"""
	从bdap.ip_detail表中获取1000个device_ip，分别在bdap.ip_ipipnet和sol.ip_net中查询该device_ip的country等字段，输出至文件
	:return:
	"""
	res1 = list()
	res2 = list()
	conn1 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	conn2 = get_mysql_connect(ip='10.0.1.188', db='sol')
	query_sql = "SELECT `device_ip` FROM `ip_detail` WHERE id BETWEEN 1 AND 1000"
	query_res = conn1.query(query_sql)
	# print(query_res)  # list
	for item in query_res:
		ip = item.get('device_ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(ip))[0])
		# print(ip, target_ip)
		location_sql1 = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_sql2 = "SELECT `country`,`province`,`city` FROM `ip_net` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res1 = conn1.query(location_sql1)
		location_res1[0]['device_ip'] = ip
		location_res2 = conn2.query(location_sql2)
		location_res2[0]['device_ip'] = ip
		# res1.append(location_res1[0])
		# res2.append(location_res2[0])
		try:
			with open(r'D:\主动探测\bdap.json', mode='a') as f1:
				f1.write(json.dumps(location_res1[0], ensure_ascii=False) + '\n')
			with open(r'D:\主动探测\sol.json', mode='a') as f2:
				f2.write(json.dumps(location_res2[0], ensure_ascii=False) + '\n')
		except Exception as e:
			continue


def result_to_mysql_S7Comm():  # result into mysql directly
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	res = NetScan.total_results('D:\Res\Res', protocol='S7Comm')
	res = NetScan.filter_results(res, conn=mongo_connect, protocol='S7Comm', timestamp='2017-01-18')
	num = 0
	print(len(res))
	for item in res:  # insert into mysql
		# try:
		# 	with open(r'D:\主动探测\result_to_mysql\s7comm_hn.json', mode='a') as f1:
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item, ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		basic_hardware = result.get('Basic Hardware')
		system_name = result.get('System Name')
		module_type = result.get('Module Type')
		module = result.get('Module')
		version = result.get('Version')
		serial_number = result.get('Serial Number')
		copyright = result.get('Copyright')

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		vendor = 'Siemens'
		insert_sql = "INSERT INTO `result_s7comm`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `basic_hardware`, `system_name`, `module_type`, `module`, `version`, `serial_number`, `copyright`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor, basic_hardware, system_name, module_type, module, version, serial_number, copyright, longitude, latitude)
		# print(insert_sql)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def result_to_mysql_Modbus():  # result into mysql directly
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	res = NetScan.total_results('D:\Res\Res', protocol='Modbus')
	res = NetScan.filter_results(res, conn=mongo_connect, protocol='Modbus', timestamp='2017-01-18')
	num = 0
	print(len(res))
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\result_to_mysql\modbus_hn.json', mode='a') as f1:
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['ip'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		vendor = result.get('Vendor')
		revision = result.get('Revision')
		device = result.get('Device')
		if vendor == 'Siemens':  # 特殊判断
			if revision is not None:
				device = device + ' ' + revision
				revision = None

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_modbus`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `revision`, `device`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor, revision,
		                device, longitude, latitude)
		# print(insert_sql)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def result_to_mysql_EtherNetIP():  # add by lhb, result into mysql directly
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	res = NetScan.total_results('D:\Res\Res', protocol='EtherNetIP')
	res = NetScan.filter_results(res, conn=mongo_connect, protocol='EtherNetIP', timestamp='2017-01-18')
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\modbus_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		vendor = result.get('Vendor')
		product_name = result.get('Product Name')
		serial_number = result.get('Serial Number')
		device_type = result.get('Device Type')
		product_code = result.get('Product Code')
		revision = result.get('Revision')


		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_ethernetip`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `product_name`, `serial_number`, `device_type`, `product_code`, `revision`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor, product_name, serial_number,  device_type, product_code, revision, longitude, latitude)
		# print(insert_sql)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def result_to_mysql_Fox():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	res = NetScan.total_results('D:\Res\Res', protocol='Fox')
	res = NetScan.filter_results(res, conn=mongo_connect, protocol='Fox', timestamp='2017-01-18')
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\fox_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item, ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
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


		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_fox`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `fox_version`, `host_name`, `application_name`, `application_version`, `vm_name`, `vm_version`, `os_name`, `time_zone`, `host_id`, `vm_uuid`, `brand_id`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, fox_version, host_name, application_name,  application_version, vm_name, vm_version, os_name, time_zone, host_id, vm_uuid, brand_id, longitude, latitude)
		# print(insert_sql)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def result_to_mysql_DNP3():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	res = NetScan.total_results('D:\Res\Res', protocol='DNP3')
	res = NetScan.filter_results(res, conn=mongo_connect, protocol='DNP3', timestamp='2017-01-18')
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\dnp3_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		destination_address = result.get('Destination Address')
		source_address = result.get('Source Address')
		control = result.get('Control')

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_dnp3`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `destination_address`, `source_address`, `control`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, destination_address, source_address, control, longitude, latitude)
		# print(insert_sql)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def result_to_mysql_Cspv4():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	res = NetScan.total_results('D:\Res\Res', protocol='Cspv4')
	res = NetScan.filter_results(res, conn=mongo_connect, protocol='Cspv4', timestamp='2017-01-18')
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\dnp3_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		session_id = result.get('Session ID')

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_cspv4`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `session_id`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, session_id, longitude, latitude)
		# print(insert_sql)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def result_to_mysql_BACnet():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	res = NetScan.total_results('D:\Res\Res', protocol='BACnet')
	res = NetScan.filter_results(res, conn=mongo_connect, protocol='BACnet', timestamp='2017-01-18')
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\bacnet_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue

		# result = item.get('result')  # mongodb里部分bacnet协议有错，将其protocol字段修改为SNMP
		# figger = result.get('figger')
		# if figger is not None:
		# 	tid = item.get('_id')
		# 	mongo_connect.update({'protocol': 'SNMP'}, 'Online', {'_id': tid})
		# 	num += 1
		# 	print(num)

		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
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

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_bacnet`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor_id`, `vendor_name`, `instance_number`, `firmware`, `application_software`, `object_name`, `object_identifier`, `model_name`, `description`, `location`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor_id, vendor_name, instance_number, firmware, application_software, object_name, object_identifier, model_name, description, location, longitude, latitude)
		# print(insert_sql)
		# if num == 88:  # 特殊字符处理
		# 	insert_sql = "INSERT INTO `result_bacnet`(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor_id`, `vendor_name`, `instance_number`, `firmware`, `application_software`, `object_name`, `object_identifier`, `model_name`, `description`, `location`, `longitude`, `latitude`) VALUES ('37', '2016-10-21 00:00:00', '61.183.8.38', '中国', '湖北', '武汉', 'Siemens Schweiz AG (Formerly: Landis & Staefa Division Europe) (7)', 'Siemens Building Technologies', 'None', 'FW=V4.00.060 / SBC=05.10 / FLI=04.00 / BBI=10.05 / STF=01.10', 'Appl_SW_Vers', 'Hovari1 AS01', '2100225', 'PXC100ED / HW=V1.00', 'PXC Contr. 01. YouYi Building', 'None', '114.2734', '30.5801')"
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def result_to_mysql_FINS():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	res = NetScan.total_results('D:\Res\Res', protocol='FINS')
	res = NetScan.filter_results(res, conn=mongo_connect, protocol='FINS', timestamp='2017-01-18')
	print(len(res))
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\fins_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue

		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
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

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_fins`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `controller_model`, `controller_version`, `for_system_use`, `program_area_size`, `iom_size`, `no_dm_words`, `timer_counter`, `expansion_dm_size`, `no_of_steps_transitions`, `kind_of_memory_card`, `memory_card_size`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, controller_model, controller_version, for_system_use, program_area_size, iom_size, no_dm_words, timer_counter, expansion_dm_size, no_of_steps_transitions, kind_of_memory_card, memory_card_size, longitude, latitude)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def result_to_mysql_IEC104():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	res = NetScan.total_results('D:\Res\Res', protocol='IEC-104')
	res = NetScan.filter_results(res, conn=mongo_connect, protocol='IEC-104', timestamp='2017-01-18')
	num = 0
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\mongo_to_mysql\iec104_result.json', mode='a') as f1:
		# 		del item['_id']
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue

		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		testfr_sent_recv = result.get('testfr sent / recv')
		startdt_sent_recv = result.get('startdt sent / recv')
		c_ic_na_1_sent_recv = result.get('c_ic_na_1 sent / recv')
		asdu_address = result.get('asdu address')

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_iec104`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `testfr_sent_recv`, `startdt_sent_recv`, `c_ic_na_1_sent_recv`, `asdu_address`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, testfr_sent_recv, startdt_sent_recv, c_ic_na_1_sent_recv, asdu_address, longitude, latitude)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def result_to_mysql_HTTP():  # add by lhb
    mongo_connect = get_connect('127.0.0.1')
    mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
    mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
    res = NetScan.total_results('D:\Res\Res', protocol='HTTP')
    res = NetScan.filter_results(res, conn=mongo_connect, protocol='HTTP', timestamp='2017-01-18')
    num = 0
    for item in res:
        # try:
        # 	with open(r'D:\主动探测\mongo_to_mysql\http.json', mode='a') as f1:
        # 		del item['_id']
        # 		item['timestamp'] = str(item['timestamp'])
        # 		f1.write(json.dumps(item['result'], ensure_ascii=False) + '\n')
        # except Exception as e:
        # 	continue

        geo = item.get('geo')
        longitude = geo[0]
        latitude = geo[1]
        device_ip = item.get('ip')
        target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
        location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
        location_res = mysql_connect2.query(location_sql)
        device_country = location_res[0]['country']
        device_province = location_res[0]['province']
        device_city = location_res[0]['city']
        # protocol = item.get('protocol')
        result = item.get('result')
        device = result.get('device')

        create_time = item.get('timestamp')
        task_id = get_taskid_by_createtime(create_time)

        insert_sql = "INSERT INTO `result_http`" \
                     "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `device`, `longitude`, `latitude`)" \
                     " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (task_id, create_time, device_ip, device_country, device_province, device_city, device, longitude, latitude)
        mysql_connect1.insert(insert_sql)
        num += 1
        print(num)


def result_to_mysql_SNMP():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	res = NetScan.total_results('D:\Res\Res', protocol='SNMP')
	res = NetScan.filter_results(res, conn=mongo_connect, protocol='SNMP', timestamp='2017-01-18')
	num = 0
	print(len(res))
	for item in res:
		# try:
		# 	with open(r'D:\主动探测\result_to_mysql\snmp_hb.json', mode='a') as f1:
		# 		item['timestamp'] = str(item['timestamp'])
		# 		f1.write(json.dumps(item['ip'], ensure_ascii=False) + '\n')
		# except Exception as e:
		# 	continue
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)
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
				print('stop')
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
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `vendor`, `brand`, `cpu`, `fireware_version`, `hardware_version`, `order_no`, `serial_number`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city, vendor, brand, cpu, fireware_version, hardware_version, order_no, serial_number, longitude, latitude)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)


def result_to_mysql_MELSEC_Q_TCP():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	res = NetScan.total_results('D:\Res\Res', protocol='MELSEC-Q-TCP')
	res = NetScan.filter_results(res, conn=mongo_connect, protocol='MELSEC-Q-TCP', timestamp='2017-01-18')
	print(len(res))
	num = 0
	for item in res:
		# print(item)
		geo = item.get('geo')
		longitude = geo[0]
		latitude = geo[1]
		device_ip = item.get('ip')
		target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		location_res = mysql_connect2.query(location_sql)
		device_country = location_res[0]['country']
		device_province = location_res[0]['province']
		device_city = location_res[0]['city']
		# protocol = item.get('protocol')
		result = item.get('result')
		cpuinfo = result.get('CPUINFO')

		create_time = item.get('timestamp')
		task_id = get_taskid_by_createtime(create_time)

		insert_sql = "INSERT INTO `result_melsec_q_tcp`" \
		             "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `cpuinfo`, `longitude`, `latitude`)" \
		             " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		             % (task_id, create_time, device_ip, device_country, device_province, device_city,cpuinfo, longitude, latitude)
		mysql_connect1.insert(insert_sql)
		num += 1
		print(num)

def result_to_mysql_MELSEC_Q_UDP():  # add by lhb
	mongo_connect = get_connect('127.0.0.1')
	mysql_connect1 = get_mysql_connect(ip='10.0.1.188', db='sol')
	mysql_connect2 = get_mysql_connect(ip='10.0.1.188', db='bdap')
	res = NetScan.total_results('D:\Res\Res', protocol='MELSEC-Q-UDP')
	res = NetScan.filter_results(res, conn=mongo_connect, protocol='MELSEC-Q-UDP', timestamp='2017-01-18')
	print(len(res))
	num = 0
	for item in res:
		print(item)
		# geo = item.get('geo')
		# longitude = geo[0]
		# latitude = geo[1]
		# device_ip = item.get('ip')
		# target_ip = socket.ntohl(struct.unpack("I", socket.inet_aton(device_ip))[0])
		# location_sql = "SELECT `country`,`province`,`city` FROM `ip_ipipnet` WHERE %s BETWEEN `ip_from` AND `ip_to`" % target_ip
		# location_res = mysql_connect2.query(location_sql)
		# device_country = location_res[0]['country']
		# device_province = location_res[0]['province']
		# device_city = location_res[0]['city']
		# # protocol = item.get('protocol')
		# result = item.get('result')
		# cpuinfo = result.get('CPUINFO')
		#
		# create_time = item.get('timestamp')
		# task_id = get_taskid_by_createtime(create_time)
		#
		# insert_sql = "INSERT INTO `result_melsec_q_udp`" \
		#              "(`task_id`, `create_time`, `device_ip`, `device_country`, `device_province`, `device_city`, `cpuinfo`, `longitude`, `latitude`)" \
		#              " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		#              % (task_id, create_time, device_ip, device_country, device_province, device_city, cpuinfo, longitude, latitude)
		# mysql_connect1.insert(insert_sql)
		# num += 1
		# print(num)

if __name__ == '__main__':
	# result_to_mongodb()
	# get_result_from_mongodb()
	result_to_mysql_HTTP()
	# get_result_from_mysql(table_name='result_http', create_time='2017-01-18')

	# tables_compare()



