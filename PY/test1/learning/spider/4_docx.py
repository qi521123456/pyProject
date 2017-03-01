from docx import Document
import requests
def readDocx(docName):
    fullText = []
    doc = Document(docName)
    paras = doc.paragraphs
    for p in paras:
        fullText.append(p.text)
    return '\n'.join(fullText)
# f = open('F:/test.docx', 'rb')
#
# print(readDocx(f))
# f.close()

def pa188():
    url = 'http://10.0.1.188:8081/sol_manager-0.0.1-SNAPSHOT/toolList'
    header = {
        'Cookie': 'JSESSIONID=53DC293CEC7DFD55CE585D7565D50D8E'
    }
    data = {'currentpage':'1'}
    r = requests.post(url,data=data,headers=header)
    print(r.text)

pa188()