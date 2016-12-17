import queue
q = queue.Queue()
for i in range(10):
    q.put(str(i)+'----in')
print(q.get(),q.get())
while not q.empty():
    print(q.get())

