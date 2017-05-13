import numpy as np
import matplotlib.pyplot as plt
def test1():
    plt.figure(figsize=(8,5), dpi=80)
    plt.subplot(111)

    X = np.linspace(-np.pi, np.pi, 256,endpoint=True)
    C = np.cos(X)
    S = np.sin(X)

    plt.plot(X, C, color="blue", linewidth=2.5, linestyle="-", label="cosine")
    plt.plot(X, S, color="red", linewidth=2.5, linestyle="-",  label="sine")

    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',0))

    plt.xlim(X.min() * 1.1, X.max() * 1.1)
    plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
      [r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])

    plt.ylim(C.min() * 1.1, C.max() * 1.1)
    plt.yticks([-1, +1],
      [r'$-1$', r'$+1$'])

    plt.legend(loc='upper left')

    plt.show()

def test2():
    # 添加主题样式
    #plt.style.use('mystyle')
    # 设置图的大小，添加子图
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111)
    # 绘制sin, cos
    x = np.arange(-np.pi, np.pi, np.pi / 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    sin, = ax.plot(x, y1, color='red', label='sin')
    cos, = ax.plot(x, y2, color='blue', label='cos')
    ax.set_ylim([-1.2, 1.2])
    # 第二种方式 拆分显示
    sin_legend = ax.legend(handles=[sin], loc='upper right')
    ax.add_artist(sin_legend)
    ax.legend(handles=[cos], loc='lower right')
    plt.show()
    import numpy as np
    import matplotlib.pyplot as plt
    # 添加主题样式
    plt.style.use('mystyle')
    # 设置图的大小，添加子图
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111)
    for color in ['red', 'green']:
        n = 750
        x, y = np.random.rand(2, n)
        scale = 200.0 * np.random.rand(n)
        ax.scatter(x, y, c=color, s=scale,
                   label=color, alpha=0.3,
                   edgecolors='none')
    ax.legend()
    ax.grid(True)
    plt.show()

if __name__ == '__main__':
    test2()