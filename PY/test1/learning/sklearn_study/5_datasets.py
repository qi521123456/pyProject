from __future__ import print_function   # 在旧版中使用新版本
from sklearn import datasets
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
loaded_data = datasets.load_boston()
data_X = loaded_data.data
# print(data_X)
data_y = loaded_data.target
model = LinearRegression()  # 回归连续
model.fit(data_X[4:,:], data_y[4:])

print(data_X[:4,:])
print(model.predict(data_X[:4, :]))
print(data_y[:4])

X, y = datasets.make_regression(n_samples=100, n_features=1, n_targets=1, noise=100)
print(X)
print(y)
plt.scatter(X, y)
plt.show()