import time
class A:
    def __init__(self):
        print('begin')

    def test(self):
        print('test')

    def __del__(self):
        time.sleep(10)
        print('end')
l = []
i = 5
while i:
    i -= 1
    if i == 3:
        l[i].test()
    a = A()
    l.append(a)
    a.test()
