import math
def perfectNum(n):
    i = 1
    sumN = 0
    while i <= int(math.sqrt(n)):
        if n % i == 0:
            sumN += i+n//i
        i += 1
    if sumN == 2*n:
        return True
    else:
        return False
#print(perfectNum(111))

def jump(n):
    i = 0
    count = 0
    while i <= n//2:
        count += (n - 2*i + 1)**i
        i += 1
    return count

print(jump(5))

