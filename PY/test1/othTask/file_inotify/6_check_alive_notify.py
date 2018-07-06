import os
check_cmd = 'ps aux | grep "python /home/monitor/watch/watch.py" | grep -v grep | wc -l'
run_watch = 'python /home/monitor/watch/watch.py'
read = os.popen(check_cmd).read()
if read=='0':
    os.popen(run_watch)
elif read=='1':
    print('alive')
else:
    os.system("kill -s 9 `ps aux | grep 'python /home/monitor/watch/watch.py' | grep -v grep| awk '{print $2}'`")
    os.popen(run_watch)
