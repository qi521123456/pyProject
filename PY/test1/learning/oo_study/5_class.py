class Solution:
    # 返回对应char

    def FirstAppearingOnce(self):
        # write code here
        l = self.l
        while self.Insert():
            s = list(set(l))
            print(s)
        for i in s:
            if l.count(i) == 1:
                return i
        return '#'

    def Insert(self, char):
        # write code here
        self.l.append(char)

if __name__ == '__main__':
    sol = Solution()
    sol.l=['g','o','o','g','l','e']
    sol.FirstAppearingOnce()