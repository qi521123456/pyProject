import os,re,time,sys
import pymysql
import shutil

def port2mysql(path):
    conn = pymysql.connect(host='10.0.1.199',
                    port=3306,
                    user='root',
                    password='123456',
                    db='sol_daily',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)
    table = ""
    now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    with conn.cursor() as cur:
        for filename in os.listdir(path):
            extN = filename.rfind(".")
            ext = filename[extN+1:]
            name = filename[:extN]
            if ext != "txt" or re.match("^[a-z]\d*$",name) is None:
                continue
            port = name[1:]
            with open(os.path.join(path,filename),'r') as fr:
                ips = fr.readlines()
            i_sql = "INSERT INTO `" + table + "` (`ip`,`port`,`create_time`,`update_time`) VALUES "
            for ip in ips:
                q_sql = "select id from %s where ip='%s' and port='%s'"%(table,ip.strip(),port)
                cur.execute(q_sql)
                if cur.fetchone() is None:
                    i_sql += "('"+ip+"','"+port+"','"+now+"','"+now+"'),"
                else:
                    u_sql = "UPDATE " + table + " SET create_time='"+now+"' WHRER id="+cur.fetchone()["id"]
                    cur.execute(u_sql)
                    conn.commit()
            if i_sql[-1] == ",":
                cur.execute(i_sql[:-1])
                conn.commit()

def mvfile(src,dst,key="test"):
    #os.system("mv -f %s/*%s* %s"%(src,key,dst))
    for filename in os.listdir(src):
        if re.match(".*"+key.lower()+".*",filename.lower()) is None:
            continue
        f = os.path.join(src,filename)
        shutil.copy2(f,dst)
        os.remove(f)
def main(arg,key,path="E:/13/data/",dst="/home/data/"):
    paths = []
    if not os.path.exists(path+"test1/"):
        for root, dirs, files in os.walk(path, topdown=False):
            if "test1" in dirs:
                paths.append(root)
    print(paths)
    tests = ["test1","test2","test3"]
    for j in paths:
        for i in tests:
            if arg==1:
                port2mysql(os.path.join(j,i))
            elif arg==2:
                mvfile(os.path.join(j,i),dst,key)
            else:
                pass

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])


