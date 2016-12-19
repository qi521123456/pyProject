import threading
import asyncio

# @asyncio.coroutine
# def hello():
#     print('Hello world! (%s)' % threading.currentThread())
#     yield from asyncio.sleep(2)
#     print('Hello again! (%s)' % threading.currentThread())
# @asyncio.coroutine
# def out1():
#     print('--------',threading.currentThread())
# loop = asyncio.get_event_loop()
# tasks = [hello(), hello(),out1()]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()

#
# @asyncio.coroutine
# def hello():
#     print("Hello world!")
#     # 异步调用asyncio.sleep(1):
#     r = yield from asyncio.sleep(10)
#     print("Hello again!")
#
# # 获取EventLoop:
# loop = asyncio.get_event_loop()
# # 执行coroutine
# loop.run_until_complete(hello())
# loop.close()

# import asyncio
# import datetime
#
# @asyncio.coroutine
# def display_date(loop):
#     end_time = loop.time() + 5.0
#     while True:
#         print(datetime.datetime.now())
#         if (loop.time() + 1.0) >= end_time:
#             break
#         yield from asyncio.sleep(1)
#
# loop = asyncio.get_event_loop()
# # Blocking call which returns when the display_date() coroutine is done
# loop.run_until_complete(display_date(loop))
# loop.close()
