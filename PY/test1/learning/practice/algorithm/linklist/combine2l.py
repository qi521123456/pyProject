
# -*- coding:utf-8 -*-
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
class Solution:
    # 返回合并后列表
    def Merge(self, pHead1, pHead2):
        # write code here
        p = None
        if pHead1 != None and pHead2 != None:
            if pHead1.val < pHead2.val:
                p = pHead1
                pHead1 = pHead1.next
            else:
                p = pHead2
                pHead2 = pHead2.next
        elif pHead1 != None and pHead2 == None:
            return pHead1
        elif pHead1 == None and pHead2 != None:
            return pHead2
        else:
            return None
        ph = p
        while pHead1 or pHead2:
            if pHead1 != None and pHead2 != None:
                if pHead1.val < pHead2.val:
                    p.next = pHead1
                    pHead1 = pHead1.next
                else:
                    p.next = pHead2
                    pHead2 = pHead2.next
            elif pHead1 != None and pHead2 == None:
                p.next = pHead1
                pHead1 = None
            else:
                p.next = pHead2
                pHead2 = None
            p = p.next
        return ph
    def merge2(self, pHead1, pHead2):
        if not pHead1:
            return pHead2
        elif not pHead2:
            return pHead1
        if pHead1.val < pHead2.val:
            p = pHead1
            q = pHead2
        else:
            p = pHead2
            q = pHead1
        while p:
            if p.val < pHead2.val:
                pre = p



if __name__ == "__main__":
    s = Solution()
    p1 = ListNode(1)
    p1.next = ListNode(4)
    p2 = ListNode(2)
    p2.next = ListNode(10)
    p = s.Merge(p1, p2)
    while p != None:
        print(p.val)
        p = p.next