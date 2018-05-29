
def rgb():
    n = int(input())
    points = []
    for i in range(n):
        line = input().split(' ')
        newline = [line[0]]
        newline.extend(list(map(int,line[1:])))
        points.append(newline)
    maxArea = 0
    for i in range(n):
        for j in range(i,n):
            for k in range(j,n):
                maxArea = max(maxArea,_triangleArea(points[i],points[j],points[k]))
    ans = str(maxArea)
    print(ans)
    print(ans[:ans.find('.')+6])
def _triangleArea(a,b,c):
    assert len(a)==4 and len(b)==4 and len(c)==4
    color = set()
    color.add(a[0])
    color.add(b[0])
    color.add(c[0])
    if len(color)==2:
        return -1
    ab = [0]
    ac = [0]
    for i in range(1,4):
        ab.append(a[i]-b[i])
        ac.append(a[i]-c[i])
    area = .0
    area += pow(ab[2]*ac[3]-ab[3]*ac[2],2)
    area += pow(ab[1]*ac[3]-ab[3]*ac[1],2)
    area += pow(ab[1]*ac[2]-ab[2]*ac[1],2)
    area = pow(area,1/2)
    area /= 2.0
    return float(area+0.0000000001)

def topKFrequent( words, k):
    """
    :type words: List[str]
    :type k: int
    :rtype: List[str]
    """
    statd = {}
    for word in words:
        if statd.get(word) is not None:
            statd[word] = statd[word] + 1
        else:
            statd[word] = 1
    res = []
    sortint = []
    for w in statd:
        sortint.append(statd[w])
    sortint.sort(reverse=True)
    for i in range(k):
        for sd in statd:
            if statd[sd] == sortint[i]:
                res.append(sd)
                statd[sd] = -1
                break
    return res
if __name__ == '__main__':
    # rgb()

    print(topKFrequent(["i", "love", "leetcode", "i", "love", "coding"],2))