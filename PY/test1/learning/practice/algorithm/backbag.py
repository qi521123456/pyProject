class bag:
    def __init__(self,w,v,x):
        self.w = w
        self.v = v
        self.x = x
def init(n,w,v):
    l = []
    while n:
        n -= 1
        b = bag(w.pop(0),v.pop(0),0)
        l.append(b)
    return l
def backbag(l,c):
    m = 0




