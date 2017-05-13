
class stack2queue:
    def __init__(self):
        self.a = []
        self.b = []
    def push(self,node):
        self.a.append(node)
        self.b = self.a[::-1]
    def pop(self):
        self.a.pop(0)
        x = self.b.pop()
        print(x)
        return x

l = ["PSH1","PSH2","PSH3","POP","POP","PSH4","POP","PSH5","POP","POP"]

te = stack2queue()
for i in l:
    #print(te.b)
    if i == 'POP' and len(te.b) != 0:
        te.pop()
    else:
        te.push(int(i[-1]))

