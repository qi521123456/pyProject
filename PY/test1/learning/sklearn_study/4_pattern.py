from sklearn import datasets
# from sklearn.cross_validation import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
import numpy as np
iris = datasets.load_iris()
iris_X = iris.data
iris_y = iris.target
# print(iris_X[:2, :])
# print(iris_y)

X_train, X_test, y_train, y_test = train_test_split(iris_X, iris_y, test_size=0.3)
# print(X_test)

knn = KNeighborsClassifier()
knn.fit(X_train,y_train)  # 训练

predict_result = knn.predict(X_test)
print(predict_result)
# print(type(np.array([2,3])))