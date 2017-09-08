import threading, time
def Myjoin():
    for _ in range(5):
        print ('hello world!',threading.current_thread().name)
        time.sleep(1)
ts = []
for i in range(5):
    t=threading.Thread(target=Myjoin)
    ts.append(t)
for i in ts:
    i.start()
    i.join()
# for i in ts:
#     i.join()
print ('hello main',threading.current_thread().name)