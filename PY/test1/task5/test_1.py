
def test_add(*args):
    s=0
    for v in args:
        #if type(v) != type(1):
        #if not isinstance(v,int):
        if not type(v) is int:
            return 'wrong value'
        s +=v
    return s
#print(test_add(1,2,3,4,5))
import asyncio

def hello():
    print("Hello world!")
    # 异步调用asyncio.sleep(1):
    asyncio.sleep(1)
    print("Hello again!")

def g(x):
   yield from range(x, 0, -1)
   yield from range(x)
def g1(x):
    for i in range(x):
        yield i

def g2(x):
    yield from range(x)
#print(list(g1(5)))
import sys
print(len(sys.argv))
