

nodeIps = {'s':0, 'a':2}
def get_down_node():  # 若5次没有收到节点状态数据则认为该节点down
    nodes = list()  # 一次可能有多个节点down
    print(nodeIps,'in def')
    for (key, value) in nodeIps:  # 带（）在200条以下性能好http://www.jb51.net/article/50507.htm
        if value == 0:
            print('i am right')
        if value >= 5:
            nodes.append(key)
            return nodes
    return None

# get_down_node()
# for (key, value) in nodeIps.items(): # items
#     print(key,value)
print(nodeIps.get('s'))