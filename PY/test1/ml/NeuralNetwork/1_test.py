# Imports
# pandas
import pandas as pd
from pandas import Series, DataFrame

# numpy, matplotlib, seaborn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

# machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics

df = pd.read_csv("./train.csv")
test = pd.read_csv("./test.csv")

df.drop(["PassengerId", "Ticket", "Name"], axis=1, inplace=True)
test.drop(["Ticket", "Name"], axis=1, inplace=True)

df['Gender'] = df['Sex'].map({'female': 1, 'male': 0}).astype(int)
test['Gender'] = test['Sex'].map({'female': 1, 'male': 0}).astype(int)

ages = np.zeros((2, 3))
ages_t = np.zeros((2, 3))
for i in range(2):
    for j in range(3):
        ages[i, j] = df[(df["Gender"] == i) & (df["Pclass"] == j + 1)]["Age"].dropna().median()
        ages_t[i, j] = test[(test["Gender"] == i) & (test["Pclass"] == j + 1)]["Age"].dropna().median()

df.drop(["Sex"], axis=1, inplace=True)
test.drop(["Sex"], axis=1, inplace=True)

df["CAge"] = df["Age"]
test["CAge"] = test["Age"]

for i in range(2):
    for j in range(3):
        df.loc[(df.Age.isnull()) & (df["Gender"] == i) & (df["Pclass"] == j + 1), "CAge"] = ages[i, j]
        test.loc[(test.Age.isnull()) & (test["Gender"] == i) & (test["Pclass"] == j + 1), "CAge"] = ages_t[i, j]

# df["Gender"] = df["Gender"] * 2
# test["Gender"] = df["Gender"] * 2

df.drop(["Age"], axis=1, inplace=True)
test.drop(["Age"], axis=1, inplace=True)

df["Nage"] = df["CAge"]
test["Nage"] = df["CAge"]

df["Age*Pclass"] = df.CAge * df.Pclass
test["Age*Pclass"] = test.CAge * test.Pclass

df.drop(["CAge"], axis=1, inplace=True)
test.drop(["CAge"], axis=1, inplace=True)

df.drop(["Pclass"], axis=1, inplace=True)
test.drop(["Pclass"], axis=1, inplace=True)

df["Embarked"].fillna("S", inplace=True)
test["Embarked"].fillna("S", inplace=True)

df['FamilySize'] = df['SibSp'] + df['Parch']
test['FamilySize'] = test['SibSp'] + test['Parch']

df.drop(["SibSp", "Parch", "Cabin"], axis=1, inplace=True)
test.drop(["SibSp", "Parch", "Cabin"], axis=1, inplace=True)

df["Embarked"] = df["Embarked"].map({'S': 0, 'C': 1, 'Q': 2}).astype(int)
df = df.dropna()

test["Embarked"] = test["Embarked"].map({'S': 0, 'C': 1, 'Q': 2}).astype(int)
test.loc[(test.Fare.isnull()), "Fare"] = test["Fare"].dropna().mean()
# train_y["Q"] = df["NAge"]

train_y = df["Survived"]
df.drop(["Survived"], axis=1, inplace=True)

train_x = df.values
train_y = train_y.values

psid = test["PassengerId"]
print(psid.head())

test.drop(["PassengerId"], axis=1, inplace=True)
test_x_t = test.values

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(penalty='l2')
model.fit(train_x, train_y)

"""from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB(alpha=0.01)
model.fit(train_x, train_y)"""

"""from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=1000)
model.fit(train_x, train_y)    """

"""from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier(n_estimators=200)
model.fit(train_x, train_y)

nn =NeuralNetwork([64,100,10],'logistic')
X_train, X_test, y_train, y_test = train_test_split(X, y)
labels_train = LabelBinarizer().fit_transform(y_train)
labels_test = LabelBinarizer().fit_transform(y_test)
"""

predict = model.predict(test_x_t)

submission = pd.DataFrame({
    "PassengerId": psid,
    "Survived": predict
})
submission.to_csv('titanic1.csv', index=False)

plt.show()






