
def jx(n):
    if n == 0:
        return 1
    return n*jx(n-1)
def jumpFloor1(number):
    i = 1
    count = 1
    while i <= number // 2:
        j = number - 2*i
        if j>=i:
            count += jx(j+1)//(jx(i)*jx(j-i+1))
        else:
            count += jx(i+1)//(jx(j)*jx(i-j+1))
        #count += (number - 2 * i + 1) ** i
        i += 1
    return count

print(jumpFloor1(5))

print(jx(5))

class Solution:
    def jx(self,n):
        if n == 0:
            return 1
        return n*jx(n-1)

    def jumpFloor(self,number):
        i = 1
        count = 1
        while i <= number // 2:
            j = number - 2*i
            if j>=i:
                count += self.jx(j+1)//(self.jx(i)*self.jx(j-i+1))
            else:
                count += self.jx(i+1)//(self.jx(j)*self.jx(i-j+1))
            #count += (number - 2 * i + 1) ** i
            i += 1
        return count

s = Solution()
print(s.jumpFloor(5))


def jumpFloor_rank1(number):
    # write code here
    a = 1
    b = 1
    for i in range(number):
        a, b = b, a + b
    return a

print(jumpFloor_rank1(3))