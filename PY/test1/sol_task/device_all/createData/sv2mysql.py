"""
导入文件需txt格式，文件中每个字段以\t（Tab键分隔）不用写列名。
工业监控系统列表为：系统ID  IP  国籍  省份  地市  端口  系统名称    行业
漏洞列表：系统ID   漏洞描述    系统截图    漏洞细节    类型1的漏洞数量（弱口令）   类型2的漏洞数量（逻辑漏洞）  类型3的漏洞数量（SQL注入） 类型4的漏洞数量（代码执行漏洞）    类型5的漏洞数量（文件上传漏洞）    类型6的漏洞数量（入侵痕迹）
漏洞列表中某漏洞类型个数如果没有则写 0 .
注意系统表里ID是主键不可重复。
--将图片放到tomcat->webapps->ROOT->img 文件夹下，路径需与上传字段路径相同
#######################################################
用法 :python3 sv2mysql.py [option] <(导入数据.csv)文件路径>
"""
import pymysql, datetime,sys,os
import csv

HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWORD = '123456'
DATABASE = 'sol_daily'
sysType = {"燃气":"Gas","电力":"Electricity","水利":"Water","煤炭":"Coal","供热":"Heat"}
fileType = '.csv'  # 文件类型 txt则用 '.txt',其他格式暂不支持
splitRegex = ','  # 文件中分隔字段的字符，'\t'：为tab键分隔
decodeType = 'gbk'  # csv时一般为gbk（中文编码），txt时utf-8（国际统一编码），若UnicodeDecodeError可调整其他编码格式尝试
class TomysqlVul:
    def __init__(self):
        self.conn = pymysql.connect(host=HOST,
                                    port=PORT,
                                    user=USER,
                                    password=PASSWORD,
                                    db=DATABASE,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __del__(self):
        print("关闭数据库连接...")
        self.conn.close()
    def _get_data(self,filename):
        fr = open(filename,'r',encoding=decodeType)
        if filename[filename.rfind('.'):] != fileType:
            print("文件类型失效，请修改文件后坠为：“"+fileType+"”，或sv2mysql.py中的fileType参数")
            sys.exit()
        if fileType == '.csv':
            return csv.reader(fr)
        elif fileType =='.txt':
            return fr.readlines()
        else:
            return None


    def to_sysCity(self,filename):
        with self.conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE stat_system_city")
            self.conn.commit()
            print("删除原内容")
            i_sql = "INSERT INTO `stat_system_city` (`id`,`system_country`, `system_province`, `system_city`, " \
                    "`system_ip`, `system_port`, `create_time`, `update_time`, `system_name`, `system_type`) " \
                    "VALUES"
            for line in self._get_data(filename):
                if fileType == '.csv':
                    l = line
                else:
                    l = line.strip().split(splitRegex)
                ip = l[1]
                port = l[5]
                s_sql = "SELECT * FROM `stat_system_city` WHERE system_ip='%s' and system_port=%s"%(ip,port)
                cur.execute(s_sql)
                if cur.fetchone() is not None:
                    continue
                province = l[3]
                city = l[4]
                if city[-1] == '市':
                    city = city[:-1]
                elif city[-1] == '区':
                    city = city[0:2]
                if province[-1] == '省' or province[-1] == '市':
                    province = province[:-1]
                elif province[-1] == '区':
                    if province[0] == '内':
                        province = province[0:3]
                    else:
                        province = province[0:2]
                i_sql += "("+str(int(l[0]))+",'"+l[2]+"','"+province+"','"+city+"','"+l[1]+"',"+l[5]+",'"+self.now+"','"+self.now+"','"+l[6]+"','"+sysType[l[7]]+"'),"
            insert_sql = i_sql.strip(',')
            if insert_sql[-1]!=')':
                print("no insert")
                return
            cur.execute(insert_sql)
            self.conn.commit()
            print("导入完成")
    def to_induVul(self,filename):
        with self.conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE stat_industrial_vul")
            self.conn.commit()
            print("删除原内容")
            i_sql = "INSERT INTO `stat_industrial_vul` (`vul_desc`,`vul_detail`, `vul_image_url`, `vul_date`, " \
                    "`create_time`, `update_time`, `system_id`, `vul_weak_pass`, `vul_logic`," \
                    " `vul_sql_inj`, `vul_code_exec`,`vul_5`,`vul_6`) VALUES"
            for line in self._get_data(filename):
                if fileType == '.csv':
                    l = line
                else:
                    l = line.strip().split(splitRegex)
                sysId = l[0]
                s_sql = "SELECT * FROM `stat_industrial_vul` WHERE system_id=%s" % sysId
                cur.execute(s_sql)
                if cur.fetchone() is not None:
                    print("-------",l,"--------")
                    print("此条系统id重复！")
                    return
                try:
                    v1 = l[4]
                    if v1 == '':
                        v1 = 0
                except IndexError:
                    v1 = 0
                try:
                    v2 = l[5]
                    if v2 == '':
                        v2 = 0
                except IndexError:
                    v2 = 0
                try:
                    v3 = l[6]
                    if v3 == '':
                        v3 = 0
                except IndexError:
                    v3 = 0
                try:
                    v4 = l[7]
                    if v4 == '':
                        v4 = 0
                except IndexError:
                    v4 = 0
                try:
                    v5 = l[8]
                    if v5 == '':
                        v5 = 0
                except IndexError:
                    v5 = 0
                try:
                    v6 = l[9]
                    if v6 == '':
                        v6 = 0
                except IndexError:
                    v6 = 0
                i_sql += "('"+l[1]+"','"+l[3]+"','"+ l[2]+"','"+self.now+"','"+self.now+"','"+self.now+"',"+l[0]+","+str(v1)+","+str(v2)+","+str(v3)+","+str(v4)+","+str(v5)+","+str(v6)+"),"
            insert_sql = i_sql.strip(',')
            if insert_sql[-1] != ')':
                print("no insert")
                return
            cur.execute(insert_sql)
            self.conn.commit()
            print("导入完成")
def main(dataType,filename):
    if os.path.isfile(filename) and filename[filename.rfind('.'):] == fileType:
        t = TomysqlVul()
        if dataType == "-s":
            print("开始导入system表...")
            t.to_sysCity(filename)
        elif dataType == "-v":
            print("开始导入vul表...")
            t.to_induVul(filename)
        else:
            print("数据类型错误！")
            sys.exit()
    else:
        print("文件错误！")
        print("文件不存在，或文件类型失效，请修改文件后坠为：“" + fileType + "”，或sv2mysql.py中的fileType参数")
        sys.exit()
if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])

