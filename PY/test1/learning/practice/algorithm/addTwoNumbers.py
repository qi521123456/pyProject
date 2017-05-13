
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None
class LinkList(object):
    def __init__(self,data):
        self.head = ListNode(data[0])
        p = self.head
        for i in data[1:]:
            node = ListNode(i)
            p.next = node
            p = p.next


def addTwoNumbers(l1, l2):
    res = []
    n1 = l1.head
    n2 = l2.head
    while n1 is not None and n2 is not None:
        res.append((n1.val+n2.val) % 10 )
        n1 = n1.next
        n2 = n2.next
    return LinkList(res)


def addTwoNumbers_2(l1, l2):
    s1 = ''
    s2 = ''
    for i in l1[::-1]:
        s1 += (str(i))
    for j in l2[::-1]:
        s2 += (str(j))
    s3 = int(s1)+int(s2)
    print(list(str(s3)[::-1]))
addTwoNumbers_2([2, 4, 7], [3, 6, 1])
n1 = LinkList([2, 4, 7])
n2 = LinkList([3, 6, 1])
#print(addTwoNumbers(n1,n2).head.val)

# ----------------------------------------print linklist

