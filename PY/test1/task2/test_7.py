from task2.common import *
mi=mongodb.MongoDBInterface()
xh=xml_util.XMLHandler('D:/test_update.xml')
mi.connect('127.0.0.1','SOL','limengqi','limengqi')
root=xh.get_root()
elements=xh.get_elements(root,'student')
for elem in elements:
    sId=xh.get_attr_value_by_name(elem,'no')
    name=xh.get_element_value(xh.get_element(elem,'name'))
    age=xh.get_element_value(xh.get_element(elem,'age'))
    gender=xh.get_element_value(xh.get_element(elem,'gender'))
    insertdict = {'sId':sId,'name':name,'age':age,'gender':gender}
    childelem=xh.get_children(elem,'score')
    sd={}
    for child in childelem:
        subject=xh.get_attr_value_by_name(child,'subject')
        score=xh.get_element_value(child)
        sd[subject]=score
    insertdict['score']=sd
    mi.insert(insertdict,'students',None)
mi.disconnect()