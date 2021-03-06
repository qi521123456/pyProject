import matplotlib.pyplot as plt

# example 1:
###############################
plt.figure(figsize=(6, 4))
plt.title("aaa")
# plt.subplot(n_rows, n_cols, plot_num)
plt.subplot(2, 2, 1)  # 讲figure分为2行2列，当前位置1
plt.title("bbb")
plt.plot([0, 1], [0, 1])

plt.subplot(2,2,2)  # 相当于plt.subplot(2,2,2)
plt.plot([0, 1], [0, 2])

plt.subplot(2,2,3)
plt.plot([0, 1], [0, 3])

plt.subplot(2,2,4)
plt.plot([0, 1], [0, 4])

plt.tight_layout()

# example 2:
###############################
plt.figure(figsize=(6, 4))
# plt.subplot(n_rows, n_cols, plot_num)
plt.subplot(2, 1, 1)
# figure splits into 2 rows, 1 col, plot to the 1st sub-fig
plt.plot([0, 1], [0, 1])

plt.subplot(234)
# figure splits into 2 rows, 3 col, plot to the 4th sub-fig
plt.plot([0, 1], [0, 2])

plt.subplot(235)
# figure splits into 2 rows, 3 col, plot to the 5th sub-fig
plt.plot([0, 1], [0, 3])

plt.subplot(236)
# figure splits into 2 rows, 3 col, plot to the 6th sub-fig
a = plt.plot([0, 1], [0, 4],label='hello uou yyy')
# plt.legend(prop={'family': 'Times New Roman', 'weight': 'normal','size': 10})
plt.legend(loc=0, numpoints=1)
leg = plt.gca().get_legend()
ltext  = leg.get_texts()
plt.setp(ltext, fontsize='small')
plt.tight_layout()  # 自动配适subplot

plt.savefig('/home/mannix/Desktop/ExperimentRes/%s.png'%'hello4',dpi=600)
plt.show()