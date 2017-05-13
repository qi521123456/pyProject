from pdfminer.pdfparser import PDFParser,PDFDocument,PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage, LTChar
def getdata(filename):
    with open(filename,'rb') as fr:
        parser = PDFParser(fr)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        print(doc)


if __name__ == '__main__':
    getdata("D:/t.pdf")