from docx import Document
from docx.shared import Inches
import requests
def readDocx(docName):
    fullText = []
    doc = Document(docName)
    paras = doc.paragraphs
    for p in paras:
        print(p)
        fullText.append(p.text)
    return '\n'.join(fullText)


def pa188():
    url = 'http://10.0.1.188:8081/sol_manager-0.0.1-SNAPSHOT/toolList'
    header = {
        'Cookie': 'JSESSIONID=53DC293CEC7DFD55CE585D7565D50D8E'
    }
    data = {'currentpage':'1'}
    r = requests.post(url,data=data,headers=header)
    print(r.text)

def writedocx(filename):
    recordset = [{'qty':1,'id':111,'desc':"love"}]
    document = Document()
    document.add_heading('Document Title', 0)
    p = document.add_paragraph('A plain paragraph having some ')
    p.add_run('bold').bold = True
    p.add_run(' and some ')
    p.add_run('italic.').italic = True
    document.add_heading('Heading, level 1', level=1)
    document.add_paragraph('Intense quote', style='IntenseQuote')

    document.add_paragraph(
        'first item in unordered list', style='ListBullet'
    )
    document.add_paragraph(
        'first item in ordered list', style='ListNumber'
    )

    document.add_picture('D:/1.jpg', width=Inches(1.25))

    table = document.add_table(rows=1, cols=4, style='Table Grid')
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Qty'
    hdr_cells[1].text = 'Id'
    hdr_cells[2].text = 'Desc'
    hdr_cells[3].text = '大大'
    for item in recordset:
        row_cells = table.add_row().cells
        row_cells[0].text = str(item['qty'])
        row_cells[1].text = str(item['id'])
        row_cells[2].text = item['desc']
    #table.style = 'LightShading-Accent2'
    #document.add_page_break()

    document.save(filename)

def readtable(filename):
    doc = Document(filename)
    table = doc.tables[0]
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)
if __name__ == '__main__':
    writedocx("D:/demo.docx")
