import sys
sys.path.append('/home/mannix/Documents/StudyandWork/pyProject/PY/test1/ml/AMyExperiment/ProduceArff/')
from sklearn.model_selection import train_test_split, KFold
from imblearn import over_sampling,combine
from NASAMDPSDPdata import AllData
from OverSampling import myOverSampling
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import auc,roc_curve,roc_auc_score
import numpy as np
import matplotlib.pyplot as plt
overSamplings = ["dispersion","random","smote","adasyn","smote_tomek","smote_enn"]
clfs = ["svm","nb","cart","rf"]
class Roc:
    def __init__(self,X,y,overSampling,clf):
        self.kflod = 3
        self.initTrainTest(X,y,overSampling,clf)

    def initTrainTest(self,X,y,overSampling,clf):
        self.X = X
        self.y = y
        # self.train_X, self.test_X,self.train_y, self.test_y =\
        #     train_test_split(X,y,test_size=0.4)
        self.overSampling = overSampling
        self.clf = clf
        self.scaler = preprocessing.Normalizer()

    def calc_macro_roc(self):
        cv = KFold(n_splits=self.kflod)
        print(np.shape(self.X))
        mean_tpr = 0.0
        mean_fpr = np.linspace(0, 1, 100)
        for i, (train, test) in enumerate(cv.split(self.X, self.y)):
            self.train_X = self.X[train]
            self.train_y = self.y[train]
            self.test_X = self.X[test]
            self.test_y = self.y[test]
            if np.sum(self.test_y == 'Y') < 1 or np.sum(np.array(self.train_y) == 'Y') < 1:
                self.kflod -= 1
                continue
            print(np.shape(self.train_X), np.shape(self.test_y))
            self.overSample()
            self.model()
            self.clf.fit(self.scaler.fit_transform(self.train_X), self.train_y)
            print(np.shape(self.test_X))
            pred_prob = self.clf.predict_proba(self.scaler.fit_transform(self.test_X))  # predict 是预测结果，proba是预测每个标签的概率
            # print(self.test_y,self.clf.predict(self.test_X))
            # print(pred_prob)
            fpr, tpr, thresholds = roc_curve(self.test_y, pred_prob[:, 1], pos_label='Y')
            mean_tpr += np.interp(mean_fpr, fpr, tpr)  # 对mean_tpr在mean_fpr处进行插值，通过scipy包调用interp()函数
            mean_tpr[0] = 0.0  # 初始处为0
        mean_tpr /= self.kflod  # 在mean_fpr100个点，每个点处插值插值多次取平均
        mean_tpr[-1] = 1.0  # 坐标最后一个点为（1,1）
        return mean_tpr,mean_fpr

    def overSample(self):
        print('train y shape before split',np.shape(self.train_y))
        if self.overSampling=="dispersion":
            self.train_X, self.train_y = myOverSampling().fit_sample(self.train_X,self.train_y)
        elif self.overSampling=="random":
            self.train_X, self.train_y = over_sampling.RandomOverSampler('minority').fit_sample(self.train_X,self.train_y)
        elif self.overSampling=="smote":
            self.train_X, self.train_y = over_sampling.SMOTE('minority',k_neighbors=np.sum(np.array(self.train_y)=='Y')-1).fit_sample(self.train_X,self.train_y)
        elif self.overSampling == "adasyn":
            self.train_X, self.train_y = over_sampling.ADASYN('minority',k=np.sum(np.array(self.train_y)=='Y')-1).fit_sample(self.train_X,                                                                                     self.train_y)
        elif self.overSampling == "smote_tomek":
            self.train_X, self.train_y = combine.SMOTETomek('minority',k=np.sum(np.array(self.train_y)=='Y')-1).fit_sample(self.train_X, self.train_y)
        elif self.overSampling == "smote_tomek":
            self.train_X, self.train_y = combine.SMOTEENN('minority',k=np.sum(np.array(self.train_y)=='Y')-1).fit_sample(self.train_X, self.train_y)
        else:
            pass
        print('after split',np.shape(self.train_y))
    def model(self):
        if self.clf=='svm':
            self.clf = SVC(C=4, kernel='rbf', gamma=2,probability=True)
        elif self.clf=='nb':
            self.clf = BernoulliNB()
        elif self.clf=='cart':
            self.clf=DecisionTreeClassifier()
        elif self.clf=='rf':
            self.clf = RandomForestClassifier()
        else:
            pass
    def run(self):
        cv = KFold(n_splits=self.kflod)
        print(np.shape(self.X))
        mean_tpr = 0.0
        mean_fpr = np.linspace(0, 1, 100)
        for i,(train,test) in enumerate(cv.split(self.X,self.y)):
            self.train_X = self.X[train]
            self.train_y = self.y[train]
            self.test_X = self.X[test]
            self.test_y = self.y[test]
            print(np.shape(self.train_X),np.shape(self.test_y))
            self.overSample()
            self.model()
            self.clf.fit(self.scaler.fit_transform(self.train_X),self.train_y)
            print(np.shape(self.test_X))
            pred_prob = self.clf.predict_proba(self.scaler.fit_transform(self.test_X)) # predict 是预测结果，proba是预测每个标签的概率
            # print(self.test_y,self.clf.predict(self.test_X))
            # print(pred_prob)
            fpr, tpr, thresholds = roc_curve(self.test_y, pred_prob[:, 1],pos_label='Y')
            mean_tpr += np.interp(mean_fpr, fpr, tpr)  # 对mean_tpr在mean_fpr处进行插值，通过scipy包调用interp()函数
            mean_tpr[0] = 0.0  # 初始处为0
            roc_auc = auc(fpr, tpr)
            # 画图，只需要plt.plot(fpr,tpr),变量roc_auc只是记录auc的值，通过auc()函数能计算出来
            plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))
            # print(self.calc_macro_roc(fpr,tpr))
        plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')

        mean_tpr /= self.kflod  # 在mean_fpr100个点，每个点处插值插值多次取平均
        mean_tpr[-1] = 1.0  # 坐标最后一个点为（1,1）
        mean_auc = auc(mean_fpr, mean_tpr)  # 计算平均AUC值
        print(mean_fpr,"--",mean_tpr)
        # 画平均ROC曲线
        # print mean_fpr,len(mean_fpr)
        # print mean_tpr
        plt.plot(mean_fpr, mean_tpr, 'k--',
                 label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)

        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic example')
        plt.legend(loc="lower right")
        plt.show()
if __name__ == '__main__':
    # X = []
    # y = []
    # from scipy.io import arff
    # with open("/home/mannix/Desktop/NASADefectDataset/CleanedData/MDP/D'/CM1.arff", 'r') as fr:
    #     data, meta = arff.loadarff(fr)
    #     for d in data:
    #         X.append(tuple(d)[:-1])  # 必须强转
    #         y.append(d[-1].decode())
    for data in AllData():
        name = data.get('name')
        X = np.array(data.get('X'))
        y = np.array(data.get('y'))
        # plt.figure(figsize=(6,4))
        for i,classifier in enumerate(clfs):
            # print(i,'----------')
            # plt.subplot(2,2,i+1)

            for oversmp in overSamplings:
                tprs = []
                fprs = []
                aucs = []
                for j in range(10):
                    tpr,fpr = Roc(np.array(X),np.array(y),oversmp,classifier).calc_macro_roc()
                    roc_auc = auc(fpr,tpr)
                    aucs.append(roc_auc)
                    tprs.append(tpr)
                    fprs.append(fpr)
                if oversmp=='dispersion':
                    index = aucs.index(max(aucs))
                else:
                    index = aucs.index(min(aucs))
                fpr = fprs[index]
                tpr = tprs[index]
                roc_auc = aucs[index]
                plt.plot(fpr, tpr, lw=1, label='%s (AUC=%0.2f)' % (oversmp, roc_auc*100))
            plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')
            plt.xlim([-0.05, 1.05])
            plt.ylim([-0.05, 1.05])
            # plt.xlabel('False Positive Rate')
            # plt.ylabel('True Positive Rate')
            plt.title('%s,%s'%(name,classifier))
            plt.legend(loc="lower right")
        # plt.tight_layout()
        plt.savefig('/home/mannix/Desktop/ExperimentRes/%s.png'%name)
        # plt.show()