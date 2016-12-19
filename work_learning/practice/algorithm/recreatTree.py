# coding:utf-8

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def ln2tree(pre,tin):
    if len(pre) == 0 or len(tin) == 0:
        return None
    root = TreeNode(pre[0])
    subpre = pre[1:]
    index = tin.index(root.val)
    subl = tin[:index]
    subr = tin[index+1:]
    root.left = ln2tree(subpre[:len(subl)],subl)
    root.right = ln2tree(subpre[-len(subr):],subr)
    return root

ll = [1,2,4,7,3,5,6,8]
lr = [4,7,2,1,5,3,8,6]
print(ln2tree(ll,lr).left.left.right.val)