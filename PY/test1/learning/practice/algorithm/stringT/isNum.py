import re
def isNum(s):
    #return s.isdigit()
    l = s.upper().split('E')
    if len(l) == 1:
        s1 = l[0]
        if s1[0] in ['-','+']:
            s1 = s1[1:]
        l1 = s1.split('.')
        if len(l1)>2:
            return False
        if l1[0] == '':
            l1 = l1[1:]
        if 1<=len(l1) <= 2:
            for i in l1:
                if not i.isdigit():
                    return False
            return True
        return False

    elif len(l) == 2 and l[1] != '':
        s1 = l[0]
        s2 = l[1]
        if s1[0] in ['-','+']:
            s1 = s1[1:]
        l1 = s1.split('.')
        if len(l1)>2:
            return False
        if l1[0] == '':
            l1 = l1[1:]
        if len(l1) <= 2:
            for i in l1:
                if not i.isdigit():
                    return False
        if s2[0] in ['-','+']:
            s2 = s2[1:]
        if not s2.isdigit():
            return False
        return True
    else:
        return False
def isN2(s):
    # [eE][\+\-]? 表示e或E跟上+或-最多一组
    return re.match(r"^[\+\-]?[0-9]*(\.[0-9]*)?([eE][\+\-]?[0-9]+)?$", s)

print(set({2,3,4}))