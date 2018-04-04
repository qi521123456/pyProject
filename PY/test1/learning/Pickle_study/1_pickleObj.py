import pickle

class a:
    def __init__(self):
        self.t = 1
        self.w = 2
        self.r = 3

class Task:
    def __init__(self,):
        self.taskid = 101
        self.scantype = 'port'
        self.port = 80
        self.script = ''
        self.pct = ''  # tcp or udp
        self.white = '/home/lmqdcs/v2/w.txt'
def te():
    q = pickle.dumps(Task())
    print(q)
    print(pickle.loads(q).__dict__)

if __name__ == '__main__':
    # import sys
    # arg = sys.argv
    # p = pickle.loads(eval(arg[1]))
    # print(p.w)
    te()