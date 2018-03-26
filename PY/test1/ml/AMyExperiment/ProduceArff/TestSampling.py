import numpy as np
from sklearn.model_selection import KFold
from sklearn import preprocessing
from sklearn import metrics
from sklearn.svm import SVC

from OverSampling import myOverSampling
from imblearn.over_sampling import RandomOverSampler,SMOTE,ADASYN
from imblearn.combine import SMOTEENN,SMOTETomek

def kfCV(X,y,K=5,clf = SVC(C=4, kernel='rbf', gamma=2),over_sampling=RandomOverSampler):
    kf = KFold(n_splits=K)
    k_num = K
    scaler = preprocessing.Normalizer()
    roc_auc = 0.
    precision = 0.
    recall = 0.
    f1 = 0.
    ap = 0.
    le = preprocessing.LabelEncoder()
    for i in kf.split(X):
        X_train = X[i[0]]
        y_train = y[i[0]]
        X_test = X[i[1]]
        y_test = y[i[1]]
        # print(np.sum(np.array(y_train)=='Y'))
        if np.sum(y_test=='Y')<1 or np.sum(np.array(y_train)=='Y')<1:
            k_num -= 1
            # print("no Y")
            continue

        # print(np.sum(y_train=='Y'))
        if over_sampling is not None:
            if over_sampling is SMOTE and np.sum(np.array(y_train)=='Y')<=5:
                X_train, y_train = over_sampling(ratio='minority',k_neighbors=np.sum(np.array(y_train)=='Y')-1).fit_sample(X_train, y_train)
            elif over_sampling is ADASYN and np.sum(np.array(y_train)=='Y')<=5:
                X_train, y_train = over_sampling(ratio='minority',n_neighbors=np.sum(np.array(y_train)=='Y')-1).fit_sample(X_train, y_train)
            elif over_sampling in [SMOTEENN,SMOTETomek] and np.sum(np.array(y_train)=='Y')<=5:
                X_train, y_train = over_sampling(ratio='minority',k=np.sum(np.array(y_train)=='Y')-1).fit_sample(X_train, y_train)
            else:
                X_train,y_train = over_sampling('minority').fit_sample(X_train,y_train)
        # print(np.shape(X_train))
        X_train = scaler.fit_transform(X_train)
        # print(y_train)
        # print(np.shape(y_train),np.sum(np.array(y_train)=='N'),np.sum(np.array(y_train)=='Y'))
        clf.fit(X_train,y_train)
        pred = clf.predict(scaler.fit_transform(X_test))

        # y_test = le.fit_transform(y_test)
        # pred = le.fit_transform(pred)

        roc_auc += metrics.roc_auc_score(le.fit_transform(y_test),le.fit_transform(pred),average="micro")
        # precision += metrics.precision_score(y_test,pred,average="micro")
        # recall += metrics.recall_score(y_test,pred,average='micro')
        # f1 += metrics.f1_score(y_test,pred,average="micro")

        # ap += metrics.average_precision_score(y_test,pred)
        # print(metrics.classification_report(y_test, pred))
        # except Exception as e:
        #     print(e)
        #     k_num -=1
    if k_num<=0:
        k_num =1
    # print(roc_auc/k_num,'\t',precision/k_num,'\t',recall/k_num,'\t',f1/k_num)
    print(roc_auc / k_num)



if __name__ == '__main__':
    from NASAMDPSDPdata import AllData
    from sklearn.naive_bayes import GaussianNB
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    data = AllData()
    for ovs in [RandomOverSampler, SMOTE, ADASYN, myOverSampling, SMOTETomek, SMOTEENN]:
        # if ovs in [RandomOverSampler,SMOTE]:
        #     continue
        print(ovs.__name__)

        for d in data:
            name = d.get('name')
            X = np.array(d.get('X'))
            y = np.array(d.get('y'))
            # print( name,end='\t')
            kfCV(X,y,over_sampling=ovs,clf=RandomForestClassifier())