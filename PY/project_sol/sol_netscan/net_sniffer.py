from sol_netscan.__init__ import *
import threading
from kafka import KafkaConsumer,KafkaProducer

g_logger = Logging().get_logger()


class TaskMgt:
    """Class for managing tasks"""
    task_queue = Queue(maxsize=0)
    task_list = list()
    # python类变量是用类名的引用访问，当然实例也可以访问，访问的其实是一个地址的变量。由于list.append没有另外开辟地址所以。。。

    def create_task(self, task):
        self.task_queue.put(task, block=True)
        self.task_list.append(task)

    def remove_task(self, task_id):
        task_index = -1
        for index, task in enumerate(self.task_list):
            if task.task_id == task_id:
                task_index = index
                break
        if task_index != -1:
            self.task_list.pop(task_index)
            g_logger.info("Task '%s' was removed" % task_id)
        g_logger.warn("There is no task:'%s'" % task_id)

    def get_tasks(self):
        tasks = [task.task_id for task in self.task_list]
        return tasks

    def task_status(self, task_id):
        for task in self.task_list:
            if task.task_id == task_id:
                return task.task_status.value
        g_logger.warn("Task given task_id:'%s' not in task_list" % task_id)
        return None

    def set_task_status(self, task_id, task_status):
        for task in self.task_list:
            if task.task_id != task_id:
                continue
            task.task_status = task_status
            break
    def kill_running_task(self):
        for task in self.task_list:
            if task.task_process is not None:  # 也可应status，或者传入id
                 os.killpg(task.task_process.pid, signal.SIGUSR1)  # -15 可以kill python3 ... 以及 zmap ...
                 g_logger.info("Task id : '%s' was killed" % task.task_id)
        g_logger.warn("There is no running task")


class Consumer:  # 任务队列取任务,执行任务
    @staticmethod
    def consume_task():
        tm = TaskMgt()
        task_dir = Env.task_dir
        if not os.path.exists(task_dir):
            try:
                os.makedirs(task_dir)
            except OSError:
                print('error first makedirs')
        while not tm.task_queue.empty():
            task = tm.task_queue.get()
            if not task in tm.task_list:  # 若已在remove则不能执行
                continue
            task_id = task.task_id
            ip_src = task.task_ips
            filename = Env.task_dir + str(task_id) + '/'
            try:
                os.mkdir(filename)
            except OSError:
                print('error makedirs')
            ipfile = filename + 'white.txt'
            with open(ipfile, 'w') as ips:
                ips.writelines(ip_src)  # TODO  依据task的ip_src 和 script 的类型（list，string...）写入
                ips.close()
            cmd = ['python3', '/home/qiqi/WorkFile/project_sol/sol_netscan/scan.py', task.task_strategy.value,
                   str(task.task_id), filename, str(task.port)]
            if task.task_strategy is Strategy.PROTOCOL:
                script = filename + 'script.nse'
                with open(script, 'w') as sc:
                    sc.write(task.script_data)
                    sc.close()
                cmd.append('-Pn')
                cmd.append(task.scan_pro)
                cmd.append('--script')
                cmd.append(script)
            child = subprocess.Popen(cmd, close_fds=True, preexec_fn=os.setpgrp)
            task.task_process = child
            task.task_status = TaskStatus.RUNNING
            task.task_process.communicate()
            task.task_status = TaskStatus.DONE
            task.task_process = None

            # if os.path.exists(filename+task_id+'.xml'):
            try:
                with open(filename+task_id+'.xml','r+') as xf:
                        result =xf.read()
                        xf.close()
            except IOError:
                with open(filename + task_id + '.txt', 'r+') as tf:
                    result = tf.read()
                    tf.close()
            try:
                sender = KafkaProducer(bootstrap_servers=['localhost:9092'])
                sender.send('topic-rersult', str(TaskResult(task_id,task.task_status,result)).encode('utf-8'))
            except OverflowError:
                print("send result with some error")

            try:
                shutil.rmtree(filename)
            except OSError:
                print("can't delete dirs: %s" % filename)
    @staticmethod
    def recvTask():
        consumer = KafkaConsumer('recv-topic', bootstrap_servers=['localhost:9092'])
        for message in consumer:
            print(message.value)
    @staticmethod
    def sendStatus():
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        while True:
            time.sleep(10)
            producer.send('topic-sendStatus', str(NodeStatus()).encode('utf-8'))


class Monitor:  # 发布事件,接收事件
    thread = threading.Thread(target=Consumer.consume_task)
    thread.start()

def main():
    ip_src = ["111.5.2.4/8\n", "222.2.2.2/8\n"]
    task1 = Task(1, Strategy.PORT, 80, ip_src)
    task2 = Task(2, Strategy.PORT, 433, ip_src)
    t = TaskMgt()
    t.create_task(task1)
    t.create_task(task2)
    thread1 = threading.Thread(target=Consumer.consume_task)
    thread1.start()
    print("--------test-------------")
if __name__ == "__main__":
    pass