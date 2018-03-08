import numpy as np

from sklearn import model_selection
from  sklearn import datasets
from sklearn import svm
from sklearn import metrics

iris = datasets.load_iris()
# X_train,X_test,y_train,y_test = model_selection.train_test_split(iris.data,iris.target,test_size=0.4,random_state=0)
clf = svm.SVC()
score = model_selection.cross_val_score(clf,iris.data,iris.target,cv=10,scoring='f1_macro')

print(score.mean())

predict = model_selection.cross_val_predict(clf,iris.data,iris.target,cv=10)
print(metrics.accuracy_score(iris.target,predict))
# print(metrics.average_precision_score(iris.target,predict)) 只能2分类
print(metrics.f1_score(iris.target,predict,average='macro'))
print(metrics.auc(iris.target,predict))
print(metrics.roc_curve(iris.target,predict,pos_label=2))
metrics.precision_recall_curve
print(metrics.classification_report(iris.target, predict))