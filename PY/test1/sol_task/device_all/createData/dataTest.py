"""
导入文件需txt格式，文件中每个字段以\t（Tab键分隔）不用写列名。
工业监控系统列表为：系统ID  IP  国籍  省份  地市  端口  系统名称    行业
漏洞列表：系统ID   漏洞描述    系统截图    漏洞细节    类型1的漏洞数量（弱口令）   类型2的漏洞数量（逻辑漏洞）  类型3的漏洞数量（SQL注入） 类型4的漏洞数量（代码执行漏洞）    类型5的漏洞数量（文件上传漏洞）    类型6的漏洞数量（入侵痕迹）
漏洞列表中某漏洞类型个数如果没有则写 0 .
注意系统表里ID是主键不可重复。
#######################################################
用法 :python3 sv2mysql.py [option] <(导入数据.txt)文件路径>
"""
import pymysql, datetime,sys,os

HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWORD = '123456'
DATABASE = 'sol_daily'

sysType = {"燃气":"Gas","电力":"Electricity","水利":"Water","煤炭":"Coal"}
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
    def to_sysCity(self,filename):
        with open(filename,'r',encoding="utf-8") as fr,self.conn.cursor() as cur:
            i_sql = "INSERT INTO `stat_system_city` (`id`,`system_country`, `system_province`, `system_city`, " \
                    "`system_ip`, `system_port`, `create_time`, `update_time`, `system_name`, `system_type`) " \
                    "VALUES"
            for line in fr.readlines():
                l = line.strip().split('\t')
                ip = l[1]
                port = l[5]
                s_sql = "SELECT * FROM `stat_system_city` WHERE system_ip='%s' and system_port=%s"%(ip,port)
                cur.execute(s_sql)
                if cur.fetchone() is not None:
                    continue
                i_sql += "("+str(int(l[0]))+",'"+l[2]+"','"+l[3]+"','"+l[4]+"','"+l[1]+"',"+l[5]+",'"+self.now+"','"+self.now+"','"+l[6]+"','"+sysType[l[7]]+"'),"
            insert_sql = i_sql.strip(',')
            if insert_sql[-1]!=')':
                print("no insert")
                return
            cur.execute(insert_sql)
            self.conn.commit()
            print("导入完成")
    def to_induVul(self,filename):
        with open(filename, 'r', encoding="utf-8") as fr, self.conn.cursor() as cur:
            i_sql = "INSERT INTO `stat_industrial_vul` (`vul_desc`,`vul_detail`, `vul_image_url`, `vul_date`, " \
                    "`create_time`, `update_time`, `system_id`, `vul_weak_pass`, `vul_logic`," \
                    " `vul_sql_inj`, `vul_code_exec`,`vul_5`,`vul_6`) VALUES"
            for line in fr.readlines():
                l = line.strip().split('\t')
                sysId = l[0]
                s_sql = "SELECT * FROM `stat_industrial_vul` WHERE system_id=%s" % sysId
                cur.execute(s_sql)
                if cur.fetchone() is not None:
                    print("-------",l,"--------")
                    print("此条系统id重复！")
                    return
                i_sql += "('"+l[1]+"','"+l[3]+"','"+'./image/' + l[2]+"','"+self.now+"','"+self.now+"','"+self.now+"',"+l[0]+","+l[4]+","+l[5]+","+l[6]+","+l[7]+","+l[8]+","+l[9]+"),"
            insert_sql = i_sql.strip(',')
            if insert_sql[-1] != ')':
                print("no insert")
                return
            cur.execute(insert_sql)
            self.conn.commit()
            print("导入完成")
def main(dataType,filename):
    if os.path.isfile(filename) and filename[filename.rfind('.'):]==".txt":
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
        sys.exit()
if __name__ == '__main__':
    # main(sys.argv[2],sys.argv[3])
    filename = "sss.txt"
    print( filename[filename.rfind('.'):]==".txt")