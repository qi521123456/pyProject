import xlwt,xlrd
import requests

def getData(xls):
    print("开始请求...")
    data = []
    wb = xlrd.open_workbook(xls)
    sheet = wb.sheet_by_index(0)
    for i in range(1,sheet.nrows):
        try:
            q = requests.get("http://"+sheet.row(i)[1].value,timeout=1)
            status = q.status_code
        except:
            status = ""

        data.append([sheet.row(i)[0].value,sheet.row(i)[1].value,sheet.row(i)[1].value,status])
        #print("hello")
        print(str(round(i*100/sheet.nrows,2))+"%")
    return data


def writeData(src,dst):
    data = getData(src)
    print("开始写...")
    f = xlwt.Workbook()
    sheet = f.add_sheet("sheet1")
    head = ["标题","网址","IP地址","状态"]
    for h in range(0, 4):
        sheet.write(0,h,head[h])
    for i,content in enumerate(data):
        for j in range(0,4):
            sheet.write(i+1,j,content[j])

    f.save(dst)  # 保存文件
if __name__ == '__main__':
    writeData("E:/TASK/筛选结果_2017_11_30.xlsx","E:/res.xlsx")