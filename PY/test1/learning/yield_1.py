# yield 将函数看做一个生成器generator，每次执行到yield就会把 （b） 放到iteration里
# 一个带有 yield 的函数就是一个 generator，它和普通函数不同，
# 生成一个 generator 看起来像函数调用，但不会执行任何函数代码，
# 直到对其调用 next()（在 for 循环中会自动调用 next()）才开始执行。
# 虽然执行流程仍按函数的流程执行，但每执行到一个 yield 语句就会中断，
# 并返回一个迭代值，下次执行时从 yield 的下一个语句继续执行。
# 看起来就好像一个函数在正常执行的过程中被 yield 中断了数次，
# 每次中断都会通过 yield 返回当前的迭代值。
# python3之后不再是g.next()  -->next(g)
# python3之后不再是g.next()  -->next(g)


# def fab(max):
#     n, a, b = 0, 0, 1
#     while n < max:
#         yield b
#         # print b
#         a, b = b, a + b
#         n = n + 1
# if __name__ == '__main__':
#     # for i in fab(5):
#     #     print(i)
#     f = fab(5)
#     #print(next(f),next(f),next(f),next(f),next(f))
#     #next(f)
#     print(f.send(None))

import types
def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()
print(isinstance(consumer(),types.GeneratorType))
c = consumer()
produce(c)
