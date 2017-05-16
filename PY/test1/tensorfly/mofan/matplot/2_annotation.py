import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 50)  # 50 是采样点个数，直线时只需2，但曲线需要更多
y = 2*x + 1

plt.figure(num=10, figsize=(8, 5),)
plt.plot(x, y,)

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data', 0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data', 0))

x0 = 1
y0 = 2*x0 + 1
plt.plot([x0, x0,], [0, y0,], 'g--', linewidth=2.5)  # g-- 中g为颜色，--为虚线
plt.scatter([x0, ], [y0, ], s=50, color='r')  # set dot style

plt.plot([1,3,],[2,5,],'k--', linewidth=2.5)  # x轴从1->3,y轴从2->5
# method 1:
#####################
plt.annotate(r'$2x+1=%s$' % y0, xy=(x0, y0), xycoords='data', xytext=(+50, -50),
             textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))

# method 2:
########################
plt.text(-3.7, 3, r'$This\ is\ the\ some\ text. \mu\ \sigma_i\ \alpha_t\ wo shi ceshi$',
         fontdict={'size': 16, 'color': 'k'})

plt.show()