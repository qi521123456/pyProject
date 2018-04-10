import pickle



class a:
    def __init__(self):
        self.t = 1
        self.w = 2
        self.r = 3

class Task:
    a = 1
    def __init__(self,):
        self.taskid = 101
        self.scantype = 'port'
        self.port = 80
        self.script = ''
        self.pct = ''  # tcp or udp
        self.white = '/home/lmqdcs/v2/w.txt'
def te():
    q = pickle.dumps(Task())
    ss = str(q)
    print(type(ss))
    print(pickle.loads(eval(ss)).__dict__)

if __name__ == '__main__':
    import sys
    arg = sys.argv
    print(type(int(arg[1])))
    # p = pickle.loads(eval(arg[1]))
    # print(p.__dict__)
    # te()
    # Task.a = 2
    # print(Task.a)