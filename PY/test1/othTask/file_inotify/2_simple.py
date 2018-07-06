from __future__ import print_function
from inotify import watcher
import inotify
import sys,os
import time,pymysql
import logging,logging.handlers

localIp = '192.168.205.125'
dstIp = '192.168.205.74'
mysqlIp = '192.168.205.122'


class Logging:
    def __init__(self,path):
        self.logger = logging.getLogger()
        self.shandler = logging.StreamHandler()
        file_dir = path[:path.rfind('/')]
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        self.fhandler = logging.handlers.RotatingFileHandler(path,maxBytes=10*1024*1024,backupCount=3)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    def get_logger(self):
        self.logger.setLevel(logging.INFO)
        self.shandler.setFormatter(self.formatter)
        self.fhandler.setFormatter(self.formatter)
        self.logger.addHandler(self.shandler)
        self.logger.addHandler(self.fhandler)
        return self.logger
class MysqlLog:
    def __init__(self):
        self.host = mysqlIp
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
logger = Logging(os.path.split(os.path.realpath(__file__))[0]+'/watcher.log').get_logger()
#evt_type = {'IN_ISDIR':'文件夹','IN_ACCESS':'读','IN_ATTRIB':'元数据更改','IN_CLOSE_WRITE':'写完成','IN_CLOSE_NOWRITE':'关闭','IN_CREATE':'创建','IN_DELETE':'删除','IN_DELETE_SELF':'自删','IN_MODIFY':'更改','IN_MOVE_SELF':'自移','IN_MOVED_FROM':'移走','IN_MOVED_TO':'移入','IN_OPEN':'打开'}
evt_type = {'IN_CREATE':'创建','IN_DELETE':'删除','IN_MOVED_FROM':'移动','IN_MOVED_TO':'移动'}
def watch():
    w = watcher.AutoWatcher()
    b = []
    paths = sys.argv[1:] or ['/boot','/etc','/home','/lost+found','/media','/misc','/mnt','/net','/opt','/root','/srv','/sys','/tmp','/usr','/var']

    for path in paths:
        try:
            b = w.add_all(path, inotify.IN_ALL_EVENTS)
        except OSError as err:
            logger.error('%s: %s' % (err.filename, err.strerror))
    if not len(b):
        sys.exit(1)

    try:
        # csv_file = os.path.split(os.path.realpath(__file__))[0] + '/watcher_result.csv'
        while True:

            for evt in w.read():
                masks = []
                for mask in inotify.decode_mask(evt.mask):
                    if evt_type.get(mask):
                        masks.append(evt_type.get(mask))
                fullpath = repr(evt.fullpath)
                if fullpath.find('/home/monitor')!=-1 or len(masks)==0:
                    continue
                db = MysqlLog()
                now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                db.insert(now,fullpath,' | '.join(masks),localIp)
                del db
                # with open(csv_file, 'a+') as fw:
                #     now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                #     fw.write(now+"\t"+fullpath+"\t"+' | '.join(masks)+"\n")
                # if os.path.getsize(csv_file)>=20*1024:
                #     try:
                #         csv_scp(csv_file)
                #     except Exception as e:
                #         logger.error(e)
                #logger.info(repr(fullpath)+' : '+' | '.join(masks))

    except KeyboardInterrupt:
        logger.error('interrupted!')
def csv_scp(csv_file):
    dst = 'root@%s:/home/monitor_data/watch/%s-%s.csv'%(dstIp,localIp,time.time())
    scp_cmd = 'scp %s %s' % (csv_file, dst)
    rm_cmd = 'rm -f %s' % csv_file
    touch_cmd = 'touch %s'%csv_file
    if os.path.isfile(csv_file):
        os.system(scp_cmd)
        os.system(rm_cmd)
        os.system(touch_cmd)

if __name__ == '__main__':
    watch()