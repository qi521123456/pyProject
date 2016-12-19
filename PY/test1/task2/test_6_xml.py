#coding:utf-8
import xml.etree.cElementTree as ET
tree=ET.parse('D:/test.xml')
root=tree.getroot()
tag=root.tag
print(root,tag)
for child in root:
    print(child.tag,child.attrib['no'])
for s in root.findall('student'):
    no=s.get('no')
    name=s.find('name').text
    print(no,name)
    print(s.findall('score')[0].attrib['subject'],s.findall('score')[0].text)
    print()
for age in root.iter('age'):
    new_age = int(age.text) + 1
    age.text = str(new_age)
    age.set('updated', 'yes')
#tree.write('d:/test_update.xml')
print(root.find('student'))