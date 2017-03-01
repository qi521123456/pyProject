from docx import Document

def readDocx(docName):
    fullText = []
    doc = Document(docName)
    paras = doc.paragraphs
    for p in paras:
        fullText.append(p.text)
    return '\n'.join(fullText)
f = open('F:/test.docx', 'rb')

print(readDocx(f))
f.close()