import random
import queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support

# 发送任务的队列
send_queue = queue.Queue()
# 接收任务的队列
receive_queue = queue.Queue()

def getSend():
    return send_queue

def getReceive():
    return receive_queue

# 从BaseManager中继承的QueueManager
class QueueManager(BaseManager):
    pass

def task_msater_test():
    # 把两个Queue注册到网络上，callback参数关联Queue对象
    QueueManager.register('get_send_queue', callable = getSend)
    QueueManager.register('get_receive_queue', callable = getReceive)
    # 绑定端口5000，设置验证码'abc'
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
    # 启动Queue
    manager.start()

    # 获取通过网络访问的Queue对象
    send = manager.get_send_queue()
    receive = manager.get_receive_queue()
    # 发送几个任务
    for i in range(10):
        n = random.randint(0, 10000)
        print('put task %d..' % n)
        send.put(n)

    # 从receive队列获取结果
    print('Try to receive...')
    # 获取任务
    for i in range(10):
        try:
            s = receive.get(timeout=10)
            print('Result: %s' % s)
        except Exception as e:
            if e.args == ():
                print('接收任务时异常')
            else:
                print('接收任务时异常:\n', e)
    # 关闭
    manager.shutdown()
    print('master exit.')

if __name__ == '__main__':
    freeze_support()
    task_msater_test()