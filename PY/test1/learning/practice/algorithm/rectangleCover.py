class Solution:
    def rectCover(self, number):
        # write code here
        a = 0
        b = 1
        if number == 0:
            return 0
        for _ in range(number):
            a,b = b,a+b
        return b