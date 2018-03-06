from sklearn.model_selection import train_test_split

# 生成200个句子，前100个和后100个类别分别对应1和2
X = [[u"这是", u"第1个", u"测试"]] * 100 + [[u"这是", u"第2个", u"测试"]] * 100
y = [1] * 100 + [2] * 100
# print(y)
# 随机抽取20%的测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print(len(X_train), len(X_test))

# 查看句子和标签是否仍然对应
for i in range(len(X_test)):
    print(int(X_train[i][1][1])==y_train[i])

if __name__ == "__main__":
    print([2]+[3])