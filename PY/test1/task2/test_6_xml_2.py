from task2.common import xml_util
xh=xml_util.XMLHandler('D:/test_update.xml')
root=xh.get_root()
#print(root.tag)
elements=xh.get_elements(root,'student')
#print(elements)
for elem in elements:
    #print(elem.get('no'))
    #print(xh.get_element(elem,'name').text)
    sId=xh.get_attr_value_by_name(elem,'no')
    name=xh.get_element_value(xh.get_element(elem,'name'))
    age=xh.get_element_value(xh.get_element(elem,'age'))
    gender=xh.get_element_value(xh.get_element(elem,'gender'))
    insertdict = {'sId':sId,'name':name,'age':age,'gender':gender}
    childelem=xh.get_children(elem,'score')
    sd={}
    for child in childelem:
        #print(child.get('subject'),xh.get_element_value(child))
        subject=xh.get_attr_value_by_name(child,'subject')
        score=xh.get_element_value(child)
        sd[subject]=score
    insertdict['score']=sd
    print(insertdict)