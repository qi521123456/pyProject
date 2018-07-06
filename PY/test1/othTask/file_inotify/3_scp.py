import os,sys
'''
python 3_scp.py /home/monitor_data/process/ root@192.168.205.74:/home/monitor_data/process/honeypot_db
'''
if __name__ == '__main__':
    paths = sys.argv[1:]
    src = paths[0]
    dst = paths[1]
    assert os.path.isdir(src)
    for file in os.listdir(src):
        src_file = src+'/'+file
        if not os.path.isfile(src_file):
            continue
        scp_cmd = 'scp %s %s'%(src_file,dst)
        rm_cmd = 'rm -f %s'%src_file
        os.system(scp_cmd)
        os.popen(rm_cmd)