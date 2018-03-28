import sys,os
def TestPoll():
  import subprocess
  import datetime
  import time
  print (datetime.datetime.now())
  for i in range(3):
      p=subprocess.Popen("sleep 3",shell=True)
      t = 1
      while(t <= 5):
        # time.sleep(1)
        p.poll()

        print (p.pid,p.returncode)
        t+=1
      print (os.getpid(),datetime.datetime.now())

if __name__ == '__main__':
    TestPoll()