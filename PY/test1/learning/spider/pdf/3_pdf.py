import pdfminer
from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content
# "http://pythonscraping.com/pages/warandpeace/chapter1.pdf"
#pdfFile = urlopen('http://papers.nips.cc/paper/4824-imagenet-classification-withdeep-convolutional-neural-networks.pdf')

fw = open('D:/1.txt','w',encoding='utf-8')
pdfFile = open('D:/tet.pdf','rb')
outputString = readPDF(pdfFile).encode('utf-8')
print(outputString)

fw.write(outputString.decode())
pdfFile.close()