import os,logging,sys
import time,threading
import logging.handlers
import pymysql
from kazoo.client import KazooClient

class Env:
    PATH = os.path.split(os.path.realpath(__file__))[0]
    ZookeeperHost = '192.168.205.27:2181'
    result_topic = '/taskmgt/result'
    node_topic = '/node/status'
    log = PATH+'/solServer.log'

    MysqlHost = '192.168.120.188'
    MysqlPort = 3306
    MysqlUser = 'sol'
    MysqlPwd = 'SolWi11'
    MysqlDB = 'sol_daily'
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
                                    charset='utf8mb4')
                                    #cursorclass=pymysql.cursors.DictCursor)

    def updateTaskById(self,taskId,status):
        sql = 'UPDATE `task` SET `task_status`=%s WHERE `id`=%s'%(status,taskId)
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
            print(statuss)
        for i in statuss:
            if i[0]!=2:
                return False
        return True
    def selectTaskStstus(self,taskId):
        q_sql = 'SELECT `task_status` FROM task WHERE id=%s'%taskId
        with self.conn.cursor() as cur:
            cur.execute(q_sql)
            status = cur.fetchone()[0]
        return status
    def updateDetailStatus(self,taskId,nodeIp,index,status,resultName=None):
        q_sql = 'SELECT id FROM node WHERE node_ip="%s"'%nodeIp
        with self.conn.cursor() as cur:
            cur.execute(q_sql)
            nodeId = cur.fetchone()[0]
            if resultName:
                u_sql = 'UPDATE `task_detail` SET `task_status`=%s,file_location="%s" WHERE `task_id`=%s and ' \
                        'node_id=%s and task_detail_index=%s' % (status, resultName,taskId, nodeId, index)
            else:
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
                if ip[0] in nodeIps:
                    u_sql = 'UPDATE node SET node_status=1 WHERE node_ip="%s" and node_status=0'% ip[0]
                else:
                    u_sql = 'UPDATE node SET node_status=0 WHERE node_ip="%s" and node_status=1'% ip[0]
                print(u_sql)
                cur.execute(u_sql)
                self.conn.commit()
    def __del__(self):
        self.conn.close()

class Monitor:

    def resultWatcher(self):
        thread_node = threading.Thread(target=self.nodeWatcher)
        thread_node.start()
        try:
            imysql = Imysql()
            @zk_client.DataWatch(Env.result_topic)
            def watch_task(data, stat):
                try:
                    result = eval(data.decode())
                    print(result)
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
                        if status == 'running':
                            imysql.updateDetailStatus(taskId,nodeIp,detailIndex,1)
                            if imysql.selectTaskStstus(taskId)==0:
                                imysql.updateTaskById(taskId,1)
                                logger.info('task %s is running'%taskId)
                        elif status == 'done':
                            imysql.updateDetailStatus(taskId,nodeIp,detailIndex,2,result['result_name'])
                            if imysql.isTaskDone(taskId):
                                imysql.updateTaskById(taskId,2)
                                logger.info('task %s is done'%taskId)
                        else:
                            pass
                    else:
                        logger.info('message not success : %s'%result)
                except:
                    return
            while True:
                time.sleep(1800)
        except Exception as ex:
            logger.error(ex)
    def nodeWatcher(self):

        try:
            imysql = Imysql()
            @zk_client.ChildrenWatch(Env.node_topic)
            def node_watch(chindren):
                print(chindren)
                imysql.updateNodeStatus(chindren)

            while True:
                time.sleep(1800)
        except Exception as e:
            logger.error(e)

if __name__ == '__main__':

    global zk_client
    try:
        zk_client = KazooClient(hosts=Env.ZookeeperHost)
        zk_client.start()
    except:
        print('can`t connect to zookeeper %s, try again' % Env.ZookeeperHost)
        sys.exit(0)
    Monitor().resultWatcher()
