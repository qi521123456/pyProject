from othTask.task2.common import *
xh=xml_util.XMLHandler('D:/test/10.21/res_Enet.xml')
mi=mongodb.MongoDBInterface()
mi.connect('127.0.0.1','SOL','limengqi','limengqi')
root=xh.get_root()
elements=xh.get_elements(root,'host')
i=0
for elem in elements:
    i += 1
    selem=xh.get_element(xh.get_element(xh.get_element(elem,'ports'),'port'),'script')
    try:
        childelem=xh.get_children(selem,'elem')
    except AttributeError:
        pass
        print('nothing..attributeError....',i)
    #if childelem is None:
        #continue
    else:
        ip=xh.get_attr_value_by_name(xh.get_element(elem,'address'),'addr')
        protocol=xh.get_attr_value_by_name(selem,'id')
        #print(ip,childelem)
        result = {}
        for child in childelem:
            key=xh.get_attr_value_by_name(child,'key')
            value=xh.get_element_value(child)
            result[key] =value
        insertdict={'ip':ip,'result':result,'protocol':protocol}
        if result!={}:
            print(insertdict)
        else:
            print('没有内容，但不是attributeError！',i)
mi.disconnect()