from pykafka import KafkaClient
import time,os
import threading
import zipfile

client = KafkaClient()
TOPIC = 'test'
PATH = 'D:/test_kafka/'
nodeIps = dict()  # 节点状态key=nodeIP，value=未收到信息的次数

def count_ips():  # 在另一个线程中,每2秒ip计数加一（2秒是nodestatus发送时间间隔）
    while True:
        time.sleep(2)
        print(nodeIps)
        for key in nodeIps:
            nodeIps[key] += 1


def del_down_node():  # 若5次没有收到节点状态数据则认为该节点down,在线程中监视可设置sleep（）
    downNodes = list()  # 一次可能有多个节点down
    while True:
        #  time.sleep(2)
        for (key, value) in nodeIps.items():  # 带（）在200条以下性能好http://www.jb51.net/article/50507.htm
            if value >= 5:
                downNodes.append(key)
        if downNodes is not None:
            # TODO --改数据库节点状态--
            for ip in downNodes:  # 删除down节点，否则会一直计数增加
                print(ip, 'is down')
                del nodeIps[ip]
                downNodes.remove(ip)  # 同时删除列表中的节点


topic = client.topics[TOPIC.encode()]
try:
    os.makedirs(PATH)
except OSError:
    print('PATH exist')

thread_count = threading.Thread(target=count_ips)   # 默默计数
thread_downNodes = threading.Thread(target=del_down_node)
thread_count.start()
thread_downNodes.start()


consumer = topic.get_simple_consumer()
for message in consumer:

    if message is not None:

        try:
            msg = eval(message.value.decode())
        except Exception:
            # msg = None
            continue
        try:
            if msg['msg_type'] == 'node_status':
                ip = msg['nodeIP']
                nodeDetail = msg['nodeDetail']
                nodeIps[ip] = 0  # 此节点有反馈则刷新
                # TODO 节点细节操作
            else:
                taskID = msg['taskID']
                taskStatus = msg['taskStatus']
                scanNode = msg['scanNode']
                taskResult = msg['taskResult']
                filepath = PATH + scanNode + '/'
                try:
                    os.mkdir(filepath)
                except OSError:
                    print("%s is exist" % filepath)
                zipfilename = filepath + taskID + '.zip'
                with open(zipfilename, 'wb') as opener:
                    opener.write(taskResult)
                f = zipfile.ZipFile(zipfilename)  # 按压缩进去的名字解压出来
                f.extractall(filepath)
                f.close()
                # TODO --数据库结果更改--
        except TypeError:
            continue

