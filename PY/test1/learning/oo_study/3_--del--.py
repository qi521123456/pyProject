import time

class A:
    def __init__(self):
        self.l = []
        print('begin')

    def test(self):
        #time.sleep(3)
        self.l.append(222)
        print('dododo')

    def __del__(self):
        #time.sleep(1)
        print('end')

j = 5
while j:
    #time.sleep(1)
    j -= 1
    a = A()
    #a.test()
    print('------------',j)
    # int(id(a),id(A()))

