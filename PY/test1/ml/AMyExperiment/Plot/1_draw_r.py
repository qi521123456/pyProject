import matplotlib
import numpy as np
import matplotlib.pyplot as plt

zhfont1 = matplotlib.font_manager.FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')

x1 = list(np.random.randint(0,200,50))
y1 = list(np.random.randint(0,500,50))
x2 = list(np.random.randint(200,500,100))
y2 = list(np.random.randint(0,500,100))
for i in range(20):
    x2.append(x1[i]+10)
    x1.append(x1[i] + 15)
    y2.append(y1[i] + 10)
    y1.append(y1[i] + 20)
fig = plt.figure()
ax1 = fig.add_subplot(111)
#设置标题
ax1.set_title('Scatter Plot')
#设置X轴标签
# plt.xlabel('X')
#设置Y轴标签
# plt.ylabel('Y')
#画散点图
ax1.scatter(x1,y1,c = ['k'],marker = '+')
ax1.scatter(x2,y2,c = ['k'],marker = '.')
#设置图标
plt.legend([u'正类',u'负类'],prop=zhfont1)

plt.xticks([])
plt.yticks([])
#显示所画的图
plt.show()