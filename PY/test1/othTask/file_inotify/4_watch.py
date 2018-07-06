import os
import time,pymysql

class MysqlLog:
    def __init__(self):
        self.host = '192.168.205.122'
        self.port = 3306
        self.username = 'root'
        self.password = 'Admin@123'
        self.database = 'honeypot'
        self.table = 'monitor_file'
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.username,
                                    password=self.password,
                                    db=self.database,
                                    charset='utf8mb4')
        self.now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    def __del__(self): # del xxx
        self.conn.commit()
        self.conn.close()
    def insert(self,update_time,file_name,operation,localIp):
        insert_sql = 'INSERT INTO %s (file_update_time,file_name,operation,create_time,tmp) VALUES ("%s","%s","%s","%s","%s")'%(self.table,update_time,file_name,operation,self.now,localIp)
        with self.conn.cursor() as cur:
            cur.execute(insert_sql)
def watch2mysql(path):
    for file in os.listdir(path):
        src_file = path+'/'+file
        if not os.path.isfile(src_file) or file[-4:]!='.csv' or time.time()-os.path.getmtime(src_file)<5:  #modify time greater than 5s
            continue
        ip = file.split('-')[0]
        with open(src_file,'r') as fr:
            db = MysqlLog()
            for line in fr:
                info = line.strip().split('\t')
                u_time = info[0]
                op_file = info[1].strip("'")
                operation = info[2]
                db.insert(u_time,op_file,operation,ip)
            del db
        rm_cmd = 'rm -f %s' % src_file
        os.system(rm_cmd)

if __name__ == '__main__':
    watch2mysql('/home/monitor_data/watch')