tid = 'q'
d = dict()
print(id(d))
d[tid] = "wer"

print(id(d))
i = 10000000
while i:
    d[i] = "qw"
    i -= 1
print(id(d))