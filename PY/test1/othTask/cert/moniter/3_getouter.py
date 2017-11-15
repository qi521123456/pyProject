import requests
import time
url = "http://www.baidu.com"
log = "/home/lmq/log/getbaidu.log"
if __name__ == '__main__':
    while(True):
        q = requests.get(url)
        if q.status_code!=200:
            with open(log,"a+") as fw:
                fw.write("[%s] 请求不到外网 ，code：'%s'\n" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), q.status_code))
        time.sleep(600)