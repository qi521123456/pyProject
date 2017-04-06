# coding=utf-8
from openpyxl import Workbook,load_workbook

def test(filename):
    wb = Workbook(filename)
    # 创建一个sheet
    #ws = wb.get_sheet_by_name('Sheet1')
    # 写入10行,每行20个
    wb.create_sheet('www')
    print(wb.get_sheet_names())
    wb.save(filename)



if __name__ == '__main__':
    test('D:/myExcelFile.xlsx')



