##############################################################
"""
  Gungnir
  FileName : agent
  Author : Li Jishuai
  Date : 2015-6-4
  His : 1.0
  Description :
        Supply Nmap agent to manage operations of nmap
        Include NmapMgmt and NmapAgentAPI
        It can be call by scheduler to execute tasks
"""
##############################################################
try:
    from jsonrpc import JSONRPCResponseManager,dispatcher
    from concurrent.futures import ThreadPoolExecutor
    from werkzeug.wrappers import Request,Response
    from werkzeug.serving import run_simple
    from libnmap.process import NmapProcess
    import requests
    import commons
    import asyncio
    import json
    import time
    import os
except Exception as e:
    print(e)
    exit()
#=========================================================================

@dispatcher.add_method
def add_task(task):
    """ Method for adding task into queue

    :Parameters:
      - 'task' : task which need to execute

    :Returns:
       Size of task_queue
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(set_callback(task))
    except:
        return commons.RetInfo(0x0003).Info
    else:
        return commons.RetInfo(0x0000).Info

@asyncio.coroutine
def set_callback(task):
    """Method for adding task and set callback function

    :Parameters:
      - 'task': task which need to execute
    """
    future = asyncio.Future()
    future.add_done_callback(callback)
    yield from NmapAgentAPI.task_queue.put(task)
    future.set_result("done")

def callback(future):
    """Method for submitting task"""
    NmapAgentAPI.executor.submit(execute_task)

def execute_task():
    """Method for setting asyncio enviroment for execution of task"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    #waiting for completion of execute function
    loop.run_until_complete(execute())
    loop.close()

@asyncio.coroutine
def execute():
    """Method for parse task and feedback result for EventServer

       1.get task from the task_queue
       2.deserialize and parse the task
       3.distribute task by the method and receive result
       4.feedback execution info for EventServer

    """
    #get task from the task_queue
    task = yield from NmapAgentAPI.task_queue.get()
    #deserialize and parse
    task = json.loads(task)
    method = task.get('method')
    res = yield from distribute_task(task,method)
    params = dict()
    params["session_id"] = task.get("params").get("session_id")
    params["tool_name"] = task.get("params").get("tool_name")
    params["method"] = task.get("method")
    params["retInfo"] = res
    #feedback execution info
    if method == "execute":
        NmapAgentAPI.state_monitor.request("send_task_id",params)
    else:
        NmapAgentAPI.state_monitor.request("send_event",params)

@asyncio.coroutine
def distribute_task(task,method):
    """Method for distribute nmap method by task

    :Parameters:
      - 'task' : task which need to execute
      - 'method' : which method need to call

    :Returns:
       RetInfo contains retCode and retValue
    """
    if method == "execute":
        try:
            command = task.get("params").get("params")
            targets = NmapMgmt.parse_for_namp(command)[0]
            options = NmapMgmt.parse_for_namp(command)[1]
            if options is None:
                options = ""
            return NmapAgentAPI.nmap_handler.execute(targets,options)
        except:
            return commons.RetInfo(0x0002).Info
    else:
        taskID = task.get("params").get("params")
        if method == "start":
            return NmapAgentAPI.nmap_handler.start(taskID)
        elif method == "finish":
            return NmapAgentAPI.nmap_handler.finish(taskID)
        elif method == "pause":
            return NmapAgentAPI.nmap_handler.pause(taskID)
        elif method == "delete":
            return NmapAgentAPI.nmap_handler.delete(taskID)
        else:
            return commons.RetInfo(0x0005).Info

@dispatcher.add_method
def get_status(task_id):
    """Method for getting the task status

    : Parameters:
      - 'task_id': id of the specific task

    : Reuturns:
        status of the task specificed by given task_id
    """
    return NmapAgentAPI.nmap_handler.get_status(task_id)

@dispatcher.add_method
def get_result(task_id):
    """Method for getting the task result

    : Parameters:
      - 'task_id': id of the specific task

    : Reuturns:
        result of the task specificed by given task_id
    """
    return NmapAgentAPI.nmap_handler.get_result(task_id)

@dispatcher.add_method
def list_plugin(tool="Nmap"):
    """Method for list all of plugins of specific tool
       Update: 2016/01/05 by WuFan

    :Parameters:
      - 'tool': name of test tool,default is Nmap

    :Returns:
        RetValue contains plugins if success else exception
    """
    return NmapAgentAPI.nmap_handler.list_plugin(tool)

@dispatcher.add_method
def get_tool_status(component="Nmap"):
    """Method for getting tool status,such as version,cpu etc.

    : Pameters:
        -'component': name of test tool

    : Returns:
        status of the specific test tool
    """
    return NmapAgentAPI.nmap_handler.get_tool_status(component)
#=========================================================================

class NmapMgmt:
    """Class for managing Nmap such start task etc.
       Use library of libnmap for managing Nmap
    """

    NMAP_OPTIONS =\
    [
      '-v', '-sn', '-sZ', '-sY', '-sX', '-sW', '-sV', '-sU', '-sT', '-sS', '-sO', '-sN', '-sM', '-sL',
      '-sI', '-sF', '-sC', '-sA', '-r', '-p', '-oX', '-oS', '-oN', '-oG', '-oA', '-n', '-max-parallelism',
      '-max-hostgroup', '-iR', '-iL', '-h', '-g', '-f', '-e', '-d', '-b', '-V', '-T', '-S', '-R', '-Pn',
      '-PY', '-PU', '-PS', '-PP', '-PO', '-PM', '-PE', '-PA', '-O', '-F', '-D', '-A', '-6', '--webxml ',
      '--version-trace', '--version-light', '--version-intensity', '--version-all', '--unprivileged',
      '--ttl', '--traceroute', '--top-ports', '--system-dns', '--stylesheet', '--spoof-mac',
      '--source-port','--send-ip', '--send-eth', '--script-updatedb', '--script-trace', '--script-help',
      '--script-args-file','--script-args', '--script', '--scanflags', '--scan-delay', '--resume',
      '--reason', '--privileged','--port-ratio', '--packet-trace', '--osscan-limit', '--osscan-guess ',
      '--open', '--no-stylesheet','--mtu', '--min-rtt-timeout', '--min-rate', '--min-parallelism',
      '--min-hostgroup', '--max-scan-delay','--max-rtt-timeout/initial-rtt-timeout', '--max-retries',
      '--max-rate', '--log-errors', '--ip-options','--iflist', '--host-timeout', '--excludefile',
      '--exclude', '--dns-servers', '--datadir', '--data-length','--badsum', '--append-output'
    ]

    def __init__(self):
        self.status = {0:"DONE",1:"READY",2:"RUNNING",3:"CANCELLED",4:"FAILED"}

    @asyncio.coroutine
    def login(self,username,password):
        """Method for authentication of these test tools such as acheron

        :Parameters:
          - 'username': name of the valid account
          - 'password': password of the valid account

        :Returns:
           True if login success else False
        """
        return commons.RetInfo(0x0005).Info

    @asyncio.coroutine
    def logout(self):
        """Method for logouting the account"""
        return commons.RetInfo(0x0005).Info

    @asyncio.coroutine
    def create(self,targets,options):
        """Creating task for execute

        :Parameters:
          - 'targets' : targets for scanning
          - 'options' : way of test

        :Returns:
           RetInfo contains retCode and retValue
        """
        task_id = int(time.time())
        if self.__check_options(options):
            taskID = NmapProcess(targets,options)
        else:
            taskID = "INVALID"
        NmapAgentAPI.task_table[task_id] = taskID
        return commons.RetValue(0x0000,task_id).Info

    @asyncio.coroutine
    def start(self,task_id):
        """Running the task to execute

        :Parameters:
          - 'taskID' : NmapProcess to be run

        :Returns:
          RetInfo if success else None
        """
        try:
            taskID = NmapAgentAPI.task_table.get(task_id)
            if taskID is None:
                return commons.RetInfo(0x0101).Info
            else:
                taskID.run_background()
        except Exception as e:
            return commons.RetValue(0x0105,str(e)).Info
        else:
            return commons.RetInfo(0x0000).Info

    @asyncio.coroutine
    def execute(self,targets,options):
        """Method for executing task
           1. create task
           2. start task
        : Parameters:
          - 'targets': ip address of target to scan
          - 'options': option of scan

        : Returns:
            result of execute task
        """
        try:
            create_res = yield from self.create(targets,options)
            task_id = create_res.get('retValue')
            taskID = NmapAgentAPI.task_table.get(task_id)
            if taskID is None:
                return commons.RetInfo(0x0101).Info
            elif taskID == "INVALID":
                pass
            else:
                yield from self.start(task_id)
        except Exception as e:
            return commons.RetValue(0x0105,str(e)).Info
        else:
            return commons.RetValue(0x0000,task_id).Info

    @asyncio.coroutine
    def finish(self,task_id):
        """Method for finishing the test task

        :Parameters:
          - 'taskID' : NmapProcess to be finished

        :Returns:
           RetInfo if success else None
        """
        try:
            taskID = NmapAgentAPI.task_table.get(task_id)
            if taskID is None:
                return commons.RetInfo(0x0101).Info
            elif taskID == "INVALID":
                NmapAgentAPI.task_table[task_id] = "FINISH"
            else:
                taskID.stop()
        except Exception as e:
            return commons.RetValue(0x0003,str(e)).Info
        else:
            return commons.RetInfo(0x0000).Info

    @asyncio.coroutine
    def delete(self,task_id):
        """Method for delete the test task

        :Parameters:
          - 'taskID' : NmapProcess to be deleted

        :Returns:
           RetInfo if success else None
        """
        try:
            taskID = NmapAgentAPI.task_table.get(task_id)
            if taskID is None:
                return commons.RetInfo(0x0101).Info
            else:
                NmapAgentAPI.task_table.pop(task_id)
        except:
            return commons.RetValue(0x0003,str(e)).Info
        else:
            return commons.RetInfo(0x0000).Info

    @asyncio.coroutine
    def reset(self,task_id):
        """Method for reset the test task

        :Parameters:
          - 'taskID' : NmapProcess to be deleted

        :Returns:
           RetInfo if success else None
        """
        return commons.RetInfo(0x0005).Info

    @asyncio.coroutine
    def pause(self,task_id):
        """Method for pause the test task

        :Parameters:
          - 'taskID' : NmapProcess to be deleted

        :Returns:
           RetInfo if success else None
        """
        result = yield from self.finish(task_id)
        return result

    def get_status(self,task_id):
        """Getting the status of specific test task

        :Parameters:
          - 'taskID' : NmapProcess need to get status

        :Returns:
          RetInfo if success else None
        """
        try:
            taskID = NmapAgentAPI.task_table.get(task_id)
            if taskID is None:
                return commons.RetInfo(0x0101).Info
            elif taskID == "INVALID":
                value = {"status":"interrupted","progress":100,"info":"Option of namp task is invalid"}
                return commons.RetValue(0x0000,value).Info
            elif taskID == "FINISH":
                value = {"status":"DONE","progress":100}
                return commons.RetValue(0x0000,value).Info
            else:
                rc = taskID.state
        except Exception as e:
            return commons.RetValue(0x0003,str(e)).Info
        else:
            value = dict()
            value['status'] = self.status.get(rc)
            value['progress'] = '100'
            if rc == 2:
                progress = taskID.progress
                if NmapAgentAPI.task_progress.get(taskID) is None:
                    NmapAgentAPI.task_progress[taskID] = {"progress":progress,"timer":1}
                else:
                    try:
                        if progress == NmapAgentAPI.task_progress.get(taskID).get("progress"):
                            if NmapAgentAPI.task_progress.get(taskID).get("timer") is 20:
                                value["info"] = "Denial of udp scan service by linux/unix at times"
                                value["status"] = "interrupted"
                            else:
                                NmapAgentAPI.task_progress[taskID]["timer"]+=1
                        else:
                            #avoid progress rollback
                            if float(progress) < float(NmapAgentAPI.task_progress.get(taskID).get("progress")):
                                progress = NmapAgentAPI.task_progress.get(taskID).get("progress")
                            else:
                                NmapAgentAPI.task_progress[taskID]["progress"] = progress
                            NmapAgentAPI.task_progress[taskID]["timer"] = 1
                    except:
                        pass
                value['progress'] = progress
            return commons.RetValue(0x0000,value).Info

    def get_result(self,task_id):
        """Getting the result of specific test task

        :Parameters:
         - 'taskID' : NmapProcess which to be gotten result

        :Returns:
            RetInfo if success else None
        """
        try:
            taskID = NmapAgentAPI.task_table.get(task_id)
            if taskID is None:
                return commons.RetInfo(0x0101).Info
            else:
                scan_res = taskID.stdout
        except Exception as e:
            return commons.RetValue(0x0003,str(e)).Info
        else:
            return commons.RetValue(0x0000,scan_res).Info

    def list_plugin(self,tool="Nmap"):
        """Method for list all of plugins of specific tool
           Update: 2016/01/05 by WuFan

        :Parameters:
           - 'tool': name of test tool,default is Nmap

        :Returns:
           RetValue contains plugins if success else exception
        """
        try:
            import os
            modules=[]
            cmd="ls -l /usr/share/nmap/scripts|awk '{print $9}'"
            result=os.popen(cmd).readlines()
            for i in result:
                modules.append(i.split(".")[0])
        except:
            return commons.RetValue(0x0105,str(e)).Info
        else:
            modules.remove("\n")
            return commons.RetValue(0x0000,modules).Info

    def get_tool_status(self,component="Nmap"):
        """Method for getting tool status,such as version,cpu etc.

        : Pameters:
           -'component': name of test tool

        : Returns:
           status of the specific test tool
        """
        tool_status = dict()
        try:
            tool_status["version"] = self.__get_tool_version()
            tool_status["cpu"] = self.__get_cpu_status()
            tool_status["memory"] = self.__get_memory_status()
            tool_status["disk"] = self.__get_disk_status()
            tool_status["time"] = self.__get_tool_time()
        except:
            pass
        finally:
            return commons.RetValue(0x0000,tool_status).Info

    def __get_cpu_status(self):
        """Method for getting cpu status of tool"""
        try:
            command = "ps aux | awk 'BEGIN{size=0}{if($11==nmap){size+=$3}}END{print size}'"
            cpu_info = os.popen(command).read()
            return int(float(cpu_info))
        except:
            return ""

    def __get_memory_status(self):
        """Method for getting memory status of tool"""
        try:
            command = "ps aux | awk 'BEGIN{size=0}{if($11==nmap){size+=$4}}END{print size}'"
            memory_info = os.popen(command).read()
            return int(float(memory_info))
        except:
            return ""

    def __get_disk_status(self):
        """Method for getting disk status of tool"""
        try:
            path = "/usr/share/nmap/"
            command="du "+path+" | awk 'BEGIN{size=0}{size+=$1}END{print size}'"
            disk_info = os.popen(command).read()
            return int(float(disk_info))
        except:
            return ""

    def __get_tool_time(self):
        """Method for getting time of tool"""
        try:
            import time
            time_sec = time.time()
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_sec))
        except:
            return ""

    def __get_tool_version(self):
        """Method for getting version of tool"""
        try:
            version_info = os.popen("nmap --version").read()
            version = version_info.split("\n")[1]
            return version
        except:
            return "Nmap 6.40"

    def __check_options(self,options):
        """Method for checking valid of options

        :Parameters:
           - 'options': option of nmap task

        :Returns:
           True if valid else False
        """
        options = options.split(" ")
        for option in options:
            if option not in NmapMgmt.NMAP_OPTIONS:
                return False
        return True

    @staticmethod
    def parse_for_namp(command):
        """Method for formatting command to needed style

        : Parameters:
           - 'command' : standard instruction for nmap

        :Returns:
           tuple which contains by targets and options
        """
        import re
        pattern = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
        ips = pattern.findall(command)
        if ips:
            targets = command[command.index(ips[0]):len(command)]
            command = command[0:command.index(ips[0])]
            options = None
            if '-' in command:
                options = command[command.index('-'):len(command)].strip(' ')
        return targets,options

#=========================================================================
class NmapAgentAPI:
    """Supplying task queue for executing test task
       Maintain rpc server for calling by scheduler

    :Attributes:
       - 'executor': ThreadPool for execute task
       - 'task_queue': PriorityQueue for put and get task
       - 'nmap_handler': instance of NmapMgmt
       - 'state_monitor': JSON-RPC client for send request for EventServer
       - 'task_table': dict for maintain the task_id
    """
    executor = ThreadPoolExecutor(max_workers=1)
    task_queue = asyncio.PriorityQueue()
    nmap_handler = NmapMgmt()
    task_progress = dict()
    state_monitor = None
    task_table = None

    def __init__(self,host='localhost',port=8000,monitor_ip='172.17.42.1'):
        ip_address = commons.get_ip("eth0",None)
        if ip_address is None:
            exit()
        else:
            self.host, self.port = ip_address, port
            NmapAgentAPI.task_table = dict()
            NmapAgentAPI.state_monitor = commons.BaseProxy(monitor_ip,9000)

    @Request.application
    def application(self,request):
        """Method for handle JSON-RPC request"""
        try:
            response = JSONRPCResponseManager.handle(request.data,dispatcher)
            return Response(response.json,mimetype="application/json")
        except:
            return commons.RetInfo(0x0003)

    def run_server(self):
        """Method for running the application
           It is the JSON-RPC Server
        """
        try:
            run_simple(self.host,self.port,self.application,threaded=True)
        except Exception as e:
            exit()

#=========================================================================
#main function
if __name__ == '__main__':
    import sys
    args = sys.argv
    if len(args) is 2:
        NmapAgentAPI(monitor_ip=args[1]).run_server()
    else:
        NmapAgentAPI().run_server()
