import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3,3,50)
y1 = 2*x+1
y2 = x**2

# plt.figure()  # 一个图一个figure()
# plt.plot(x,y1)

plt.figure(num=3,figsize=(8,5))
plt.title("tu san")
l1, = plt.plot(x,y2,label='liner line')  # label 图例
l2, = plt.plot(x,y1,color='red',linewidth=2.0,linestyle='--')
# plt.legend(loc='upper right')  # 显示图例
plt.legend(handles=[l1, l2], labels=['up', 'down'],  loc='best')  # 用l1，l2标记
plt.xlim((-1, 2))
plt.ylim((-2, 3))
new_ticks = np.linspace(-1, 2, 5)
plt.xticks(new_ticks)
plt.yticks([-2, -1.8, -1, 1.22, 3],['$really\ bad$', '$bad$', '$normal$', '$good$', '$really\ good$'])
ax = plt.gca()  # 获取当前坐标轴信息
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')  # x轴刻度'|'标记在底部
ax.spines['bottom'].set_position(('data', 0))  # x轴放到y=0处
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(15)  # 坐标轴标记字体大小
    label.set_bbox(dict(facecolor='black', edgecolor='red', alpha=0.7))  # 标记
plt.show()