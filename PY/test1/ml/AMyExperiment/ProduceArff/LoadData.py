from scipy.io import arff
import numpy as np
from sklearn import svm
from sklearn import preprocessing
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import NearestNeighbors
PATH = "/home/mannix/Desktop/NASADefectDataset/CleanedData/MDP/D'/CM1.arff"

def getData():
    from sklearn.model_selection import train_test_split
    X = []
    y = []
    with open(PATH,'r') as fr:
        data,meta = arff.loadarff(fr)
        for d in data:
            X.append(tuple(d)[:-1])  # 必须强转
            y.append(d[-1].decode())
    return train_test_split(X, y, test_size=0.2)

X_train, X_test, y_train, y_test = getData()

def pca_x(X,n=2):
    from sklearn.decomposition import PCA
    X = np.array(X,dtype='float64') # dtype 转化数字类型，pca中做减法时需要
    pca = PCA(n_components=n)
    pca.fit(X)
    x_reduce = pca.transform(X)
    return x_reduce

def statDiscre():
    from sklearn import preprocessing
    global X_train,y_train

    X = X_train
    y = np.array(y_train)

    scaler = preprocessing.MinMaxScaler()
    X = scaler.fit_transform(X)
    posi_Y_sum = np.sum(np.array(y)=='Y')
    # neg_Y_sum = np.sum(y=='N')
    pos_X = []
    org_X = []
    # neg_X = []
    a,b = np.shape(X)
    pos_X_sum = np.zeros(b)
    # neg_X_sum = np.zeros(b)
    for i,yi in enumerate(y):
        if yi == 'Y':
            pos_X.append(X[i])
            org_X.append(X_train[i])
            pos_X_sum+=X[i]
    #     else:
    #         neg_X.append(X[i])
    #         neg_X_sum+=X[i]
    # neg_X = np.array(neg_X)
    pos_X = np.array(pos_X)
    pos_m = pos_X_sum/posi_Y_sum
    # neg_m = neg_X_sum/neg_Y_sum
    tmp_X = pos_X-pos_m
    disc_X = np.dot(tmp_X.T,tmp_X)
    end_X = []
    for i in pos_X:
        end_X.append(np.dot(np.dot(i,disc_X),i.T))
    return org_X,pos_X,end_X/np.sum(end_X)

def trainBySvm(X_t,y_t):

    #import pandas
    #scaler = preprocessing.StandardScaler()
    le = preprocessing.LabelBinarizer()
    #global X_train, y_train
    parameters = {'kernel': ('linear', 'rbf'), 'C': [1,1.5, 2, 4], 'gamma': [0,0.125, 0.25, 0.5, 1, 2, 4]}
    for scaler in [preprocessing.StandardScaler(),preprocessing.MinMaxScaler(),preprocessing.Normalizer()]:
        print(scaler.__class__)
        X = scaler.fit_transform(X_t)
        #for k in ['linear', 'poly', 'rbf', 'sigmoid']:
        #clf = svm.SVC(kernel=k)
        svr = svm.SVC()
        clf = GridSearchCV(svr, parameters, n_jobs=-1)
        clf.fit(X, y_t)
        #cv_result = pd.DataFrame.from_dict(clf.cv_results_)
        #print(clf.cv_results_)
        # sv = clf.support_vectors_
        # print("super_vectors:",np.shape(sv)[0]/np.shape(X)[0])
        print("best params",clf.best_params_)
        # predict = clf.predict(X_test)
        # print("auc:",metrics.roc_auc_score(le.fit_transform(y_test),le.fit_transform(predict)))

        y_pred = clf.predict(scaler.fit_transform(X_test))
        print("auc:", metrics.roc_auc_score(le.fit_transform(y_test), le.fit_transform(y_pred)))
        print(metrics.classification_report(y_true=y_test, y_pred=y_pred))


def findSV():
    '''
    支持向量包含了所有正类，所以无法用到
    :return: 
    '''
    global X_train, y_train
    scaler = preprocessing.Normalizer()
    train_X = scaler.fit_transform(X_train)
    clf = svm.SVC(kernel='rbf',gamma=0.5,C=1.0,class_weight='balanced')
    clf.fit(train_X,y_train)
    sv = clf.support_vectors_
    #print("super_vectors:",np.shape(sv))
    lable = []
    print(len(sv))
    for i in sv:
        _index = train_X.tolist().index(i.tolist())
        lable.append(y_train[_index])
        # if y_train[_index]=='Y':
        #     lable.append(i)
    print(y_train)
    print(len(lable),np.sum(np.array(lable)=='Y'),np.sum(np.array(y_train)=='Y'))
    # pred = clf.predict(X_train)
    # print(metrics.classification_report(y_train,pred))

def genNeigMat(pos_X,K):

    neig = NearestNeighbors(n_neighbors=K)
    neig.fit(pos_X)
    # print(np.shape(pos_X))

    return neig.kneighbors(pos_X)[1]

def genPerPoint(p1,p2,beta):
    p1 = np.array(p1)
    p2 = np.array(p2)
    n = np.shape(X_train)[1]
    betas = np.random.rand(n)*beta #使新点不在p1,p2连线上
    tmp_dis = (p2-p1)*betas
    return p1+tmp_dis

def genPosByDis(pn,beta):
    global X_train, y_train
    posNum = np.sum(np.array(y_train)=='Y')
    negNum = np.sum(np.array(y_train)=='N')
    posGenNum = negNum*pn-posNum  #Y/N == pn时 所需要生成Y类的数目
    org_X,pos_X,dis = statDiscre()

    dis_num = np.around(dis*posGenNum)
    dis_max = np.max(dis_num)
    # dis_num.sort()
    # print(np.sum(dis_num),np.shape(X_train))
    # print(np.argwhere(dis_num>0))
    # print(np.shape(pos_X),np.shape(dis_num))
    _K = 10 # 控制近邻数

    neigs = genNeigMat(pos_X,min(dis_max,_K))
    # print(neigs)
    gen_pos = []
    # print(dis_num)
    # dis_all = np.sum(dis_num)
    dis_gt_K = np.argwhere(dis_num>_K)

    plus_gen_num = 0
    for idx in dis_gt_K:
        plus_gen_num+=(dis_num[idx[0]]-_K)
    per_plus = plus_gen_num//(len(dis_num)-len(dis_gt_K))
    new_dis_num = dis_num+per_plus
    # print(new_dis_num)
    for i,e in enumerate(new_dis_num):
        j = 1
        while j<=min(e,_K-1):
            # print(i,"--",j)
            gen_pos.append(genPerPoint(org_X[i],org_X[neigs[i][j]],beta))
            j+=1
    y_lable = ['Y']*len(gen_pos)
    return gen_pos,y_lable

def ennClearn(X,y,k1=7,k2=10):
    neig = genNeigMat(X,k2+1)
    newX = []
    newY = []
    for i,e in enumerate(neig):
        j = 1
        count=0
        while j<=k2:
            if y[e[j]] != y[i]:
                count+=1
            j+=1
        if count<k1:
            newX.append(X[i])
            newY.append(y[i])
    return newX,newY

if __name__ == '__main__':
    ps,py = genPosByDis(.8,.2)
    ps.extend(X_train)
    py.extend(y_train)
    print(np.shape(ps),np.shape(py))
    newX,newY = ennClearn(ps,py)
    print(np.shape(newX),np.shape(newY))
    trainBySvm(ps,py)
    print("-------------------------------------------------------")
    trainBySvm(newX,newY)
