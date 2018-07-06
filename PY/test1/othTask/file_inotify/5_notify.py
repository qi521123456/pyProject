from __future__ import print_function
from inotify import watcher
import inotify
import sys,os
import time


localIp = '192.168.205.125'
dstIp = '192.168.205.74'


evt_type = {'IN_CREATE':'创建','IN_DELETE':'删除','IN_MOVED_FROM':'移动','IN_MOVED_TO':'移动'}
def watch():
    w = watcher.AutoWatcher()
    b = []
    paths = sys.argv[1:] or ['/usr','/etc','/home','/opt','/root','/tmp']

    for path in paths:
        try:
            b = w.add_all(path, inotify.IN_ALL_EVENTS)
        except OSError as err:
            print('%s: %s' % (err.filename, err.strerror))
    if not len(b):
        sys.exit(1)

    try:
        csv_file = os.path.split(os.path.realpath(__file__))[0] + '/watcher_result.csv'
        while True:

            for evt in w.read():
                masks = []
                for mask in inotify.decode_mask(evt.mask):
                    if evt_type.get(mask):
                        masks.append(evt_type.get(mask))
                fullpath = repr(evt.fullpath)
                if fullpath.find('/home/monitor')!=-1 or len(masks)==0:
                    continue
                with open(csv_file, 'a+') as fw:
                    now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    fw.write(now+"\t"+fullpath+"\t"+' | '.join(masks)+"\n")
                if os.path.getsize(csv_file)>=20*1024:
                    try:
                        csv_scp(csv_file)
                    except Exception as e:
                        print(e)

    except KeyboardInterrupt:
        print('interrupted!')
def csv_scp(csv_file):
    dst = 'root@%s:/home/monitor_data/watch/%s-%s.csv'%(dstIp,localIp,time.time())
    scp_cmd = 'scp %s %s' % (csv_file, dst)
    rm_cmd = 'rm -f %s' % csv_file
    touch_cmd = 'touch %s'%csv_file
    if os.path.isfile(csv_file):
        os.system(scp_cmd)
        os.system(rm_cmd)
        os.system(touch_cmd)

if __name__ == '__main__':
    watch()