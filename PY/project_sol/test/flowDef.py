"""
def kill_1():  # 传入id也可以，但由于只有一个在运行所以可以用process的状态查询，无法测试
    t = TaskMgt()
    print(t.task_list)
    for task in TaskMgt.task_list:
        if task.task_process is not None:
             os.killpg(task.task_process.pid, signal.SIGUSR1)  # -15 可以kill python3 ... 以及 zmap ...
             print("i kill it")
def kill_2():
    for task in TaskMgt.task_list:
        if task.task_process is not None:
            zmap_cmd = 'zmap -B 1M -p '+task.port+' -w '+Env.task_dir+task.task_id+'/white.txt -o '+\
                       Env.task_dir+task.task_id+'/'+task.task_id+'.txt'
    query_cmd = r"ps aux | awk '/%s$/{print $2}'" % zmap_cmd.strip()
    process_id = os.popen(query_cmd).read()
    os.system("kill "+process_id)
"""