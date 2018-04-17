import os,logging,sys
import time,threading
import pymysql
from kazoo.client import KazooClient

class Env:
    PATH = os.path.split(os.path.realpath(__file__))[0]
    ZookeeperHost = '192.168.205.27'
    result_topic = '/taskmgt/result'
    node_topic = '/node/status'
    log = PATH+'/solServer.log'

    MysqlHost = 'localhost'
    MysqlPort = 3306
    MysqlUser = 'root'
    MysqlPwd = '123456'
    MysqlDB = 'dodoDemo'
class Logging:
    def __init__(self,path):
        self.logger = logging.getLogger()
        self.shandler = logging.StreamHandler()
        file_dir = path[:path.rfind('/')]
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        self.fhandler = logging.handlers.RotatingFileHandler(path,maxBytes=1024*1024,backupCount=3)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    def get_logger(self):
        self.logger.setLevel(logging.INFO)
        self.shandler.setFormatter(self.formatter)
        self.fhandler.setFormatter(self.formatter)
        self.logger.addHandler(self.shandler)
        self.logger.addHandler(self.fhandler)
        return self.logger
logger = Logging(Env.log).get_logger()
class Imysql:
    def __init__(self):
        self.conn = pymysql.connect(host=Env.MysqlHost,
                                    port=Env.MysqlPort,
                                    user=Env.MysqlUser,
                                    password=Env.MysqlPwd,
                                    db=Env.MysqlDB,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

    def updateTaskById(self,taskId,status):
        sql = 'UPDATE `task` SET `task_status`=`%s` WHERE `task_id`=%s'%(status,taskId)
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            logger.error('updateTask :%s'%e)
    def isTaskDone(self,taskId):
        q_sql = 'SELECT `task_status` FROM `task_detail` WHERE `task_id`=%s'%taskId
        with self.conn.cursor() as cur:
            cur.execute(q_sql)
            statuss = cur.fetchall()
        for i in statuss:
            if i!=2:
                return False
        return True
    def selectTaskStstus(self,taskId):
        q_sql = 'SELECT `task_status` FROM task WHERE task_id=%s'%taskId
        with self.conn.cursor() as cur:
            cur.execute(q_sql)
            status = cur.fetchone()
        return status
    def updateDetailStatus(self,taskId,nodeIp,index,status):
        q_sql = 'SELECT id FROM node WHERE node_ip=%s'%nodeIp
        with self.conn.cursor() as cur:
            cur.execute(q_sql)
            nodeId = cur.fetchone()
            u_sql = 'UPDATE `task_detail` SET `task_status`=%s WHERE `task_id`=%s and ' \
                'node_id=%s and task_detail_index=%s'%(status,taskId,nodeId,index)
            cur.execute(u_sql)
        self.conn.commit()
    def updateNodeStatus(self,nodeIps):
        with self.conn.cursor() as cur:
            allIp_sql = 'SELECT node_ip FROM node'
            cur.execute(allIp_sql)
            allIps = cur.fetchall()
            for ip in allIps:
                if ip in nodeIps:
                    u_sql = 'UPDATE node SET node_status=1 WHERE node_ip=%s and status=0'% ip
                else:
                    u_sql = 'UPDATE node SET node_status=0 WHERE node_ip=%s and status=1'% ip
                cur.execute(u_sql)
        self.conn.commit()
    def __del__(self):
        self.conn.close()

class Monitor:

    def resultWatcher(self):
        thread_node = threading.Thread(target=self.nodeWatcher)
        thread_node.start()
        try:
            @zk_client.DataWatch(Env.result_topic)
            def watch_task(data, stat):
                try:
                    result = eval(data.decode())
                    if (type(result) is dict) and result['message']=='success':
                        names = result['result_name'].split('-')
                        status = result.get('task_status')
                        detailIndex = 1
                        if len(names)==3:
                            taskId = names[0]
                            detailIndex = names[1]
                            nodeIp = names[2].split('@')[1]
                        elif len(names)==2:
                            taskId = names[0]
                            nodeIp = names[1].split('@')[1]
                        else:
                            return
                        if  status == 'running':
                            imysql.updateDetailStatus(taskId,nodeIp,detailIndex,1)
                            if imysql.selectTaskStstus(taskId)==0:
                                imysql.updateTaskById(taskId,1)
                        elif status == 'done':
                            imysql.updateDetailStatus(taskId,nodeIp,detailIndex,2)
                            if imysql.isTaskDone(taskId):
                                imysql.updateTaskById(taskId,2)
                        else:
                            pass
                    else:
                        logger.error('message incorrect')
                except:
                    return
            while True:
                time.sleep(1800)
        except Exception as ex:
            logger.error(ex)
    def nodeWatcher(self):
        try:
            @zk_client.ChildrenWatch
            def node_watch(chindren):
                imysql.updateNodeStatus(chindren)

            while True:
                time.sleep(1800)
        except Exception as e:
            logger.error(e)
def test():
    print("is done 384",imysql.isTaskDone(384))
    print("status 384",imysql.selectTaskStstus(384))
    imysql.updateDetailStatus(384,'192.168.120.6',1,2)
    imysql.updateTaskById(384,2)
    imysql.updateNodeStatus(['123'])
if __name__ == '__main__':
    global imysql
    imysql = Imysql()
    global zk_client
    # try:
    #     zk_client = KazooClient(hosts=Env.ZookeeperHost)
    #     zk_client.start()
    # except:
    #     print('can`t connect to zookeeper %s, try again' % Env.ZookeeperHost)
    #     sys.exit(0)
    # Monitor().resultWatcher()
    test()