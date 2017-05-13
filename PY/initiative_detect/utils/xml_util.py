import xml.etree.cElementTree as ET

class XMLHandler:
    def __init__(self,file):
        try:
            self.file = file
            self.tree = ET.parse(file)
        except Exception as e:
            print(e)

    def get_root(self):
        return self.tree.getroot()

    def get_elements(self,element,xpath):
        return element.findall(xpath)

    def get_element(self,element,xpath):
        return element.find(xpath)

    def get_element_value(self,element):
        return element.text

    def get_attr_value_by_name(self,element,attr_name):
        return element.get(attr_name)

    def get_attributes(self,element):
        return element.items()

    def update_attribute(self,element,attribute,value):
        element.set(attribute,value)

    def update_text(self,element,value):
        element.text = value

    def add_child(self,parent,child_tag,child_text):
        child = ET.SubElement(parent,child_tag)
        child.text = child_text
        return child

    def del_child(self,parent,child):
        parent.remove(child)

    def get_children(self,element,tag=None):
        return element.iter(tag)

    def clear_element(self,element):
        element.clear()

    def save(self):
        self.tree.write(self.file,encoding="UTF-8",xml_declaration=True)
