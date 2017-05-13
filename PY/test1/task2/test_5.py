from task2.common import *
mI=mongodb.MongoDBInterface()
xh=xml_util.XMLHandler('D:/test_update.xml')
mI.connect(None,'SOL','limengqi','limengqi')
#print(mongoI.query(None,'User',None))
#mongoI.insert({'name':'limengqi','age':'24','tel':'18810398057','stuID':'2016111555','sex':'男'},'User',{'username':'limengqi'})



mI.disconnect()