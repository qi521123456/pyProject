import subprocess
import time
cmd = "ping baidu.com"
child = subprocess.Popen(cmd)
while 1:
    time.sleep(1)
    child.poll()  # 不加poll child是最开始的child，retcode一直为None，poll之后才会更新
    print(child.returncode)
# child.poll()
# child.wait()
# print(child.returncode)