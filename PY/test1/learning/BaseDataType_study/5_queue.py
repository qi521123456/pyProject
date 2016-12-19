import queue
q = queue.Queue(maxsize=0)
i = 3
while i:
    q.put(i)
    i -= 1

while not q.empty():
    print(q.get())