
def binof1(n):
    binstr = bin(n).replace('0b', '')
    sum = binstr.count('1')
    if n < 0:
        if n % 2 == 1:
            return 33 - sum
        else:
            r = binstr.rfind('1')
            return 32 - (sum - (len(binstr) - r - 2))
    return sum

print(binof1(-2))