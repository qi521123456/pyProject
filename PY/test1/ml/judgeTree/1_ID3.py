# -*- coding: utf-8 -*-
import numpy as np
from sklearn import tree
# from sklearn.metrics import precision_recall_curve
# from sklearn.metrics import classification_report


''''' 数据读入 '''
data = []
labels = []
with open("F:/1.txt") as ifile:
    for line in ifile.readlines():
        tokens = line.strip().split(' ')
        data.append([float(tk) for tk in tokens[:-1]])
        labels.append(tokens[-1])
x = np.array(data)
labels = np.array(labels)
y = np.zeros(labels.shape)

''''' 标签转换为0/1 '''
y[labels == 'fat'] = 1
print(x,y)

''''' 拆分训练数据与测试数据 '''
x_train = x
x_test = np.array([1.71,65])
y_train = y


''''' 使用信息熵作为划分标准，对决策树进行训练 '''
clf = tree.DecisionTreeClassifier(criterion='entropy')
print(clf)
# clf.fit(x_train, y_train)
#
# ''''' 把决策树结构写入文件 '''
# with open("F:/2.txt", 'w') as f:
#     f = tree.export_graphviz(clf, out_file=f)
#
# ''''' 系数反映每个特征的影响力。越大表示该特征在分类中起到的作用越大 '''
# print(clf.feature_importances_)
#
# '''''测试结果的打印'''
# answer = clf.predict(x_train)
# print(x_train)
# print(answer)
# print(y_train)
# print(np.mean(answer == y_train))

'''''准确率与召回率'''
# precision, recall, thresholds = precision_recall_curve(y_train, clf.predict(x_train))
# answer = clf.predict_proba(x)[:, 1]
# print(classification_report(y, answer, target_names=['thin', 'fat']))