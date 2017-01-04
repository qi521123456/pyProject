import numpy as np

# 双层神经网络算法

def nonlin(x, deriv=False):
    if (deriv == True):
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))
# 输入
x = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])
# 输出
y = np.array([[0, 0, 1, 1]]).T  # 转置
np.random.seed(1)  # 使random的数据稳定
# 权重
syn0 = 2 * np.random.random((3, 1)) - 1
for _ in range(100000):
    l0 = x
    l1 = nonlin(np.dot(l0, syn0))

    l1_error = y - l1

    l1_delta = l1_error * nonlin(l1, True)

    syn0 += np.dot(l0.T, l1_delta)
print("经神经网络算法处理后：\n",l1 )