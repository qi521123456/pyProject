import time,os
from scipy.io import arff
import numpy as np
from sklearn.model_selection import train_test_split,KFold
from sklearn.preprocessing import Normalizer
from sklearn.ensemble import IsolationForest,RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import auc,roc_curve
def processData(path):
    X = []
    y = []
    with open(path, 'r') as fr:
        data, meta = arff.loadarff(fr)
        for d in data:
            X.append(tuple(d)[:-1])  # 必须强转
            y.append(d[-1].decode())
    return np.log2(np.mat(X)+1),y
def getOriData(path):
    X = []
    y = []
    with open(path, 'r') as fr:
        data, meta = arff.loadarff(fr)
        for d in data:
            X.append(list(d)[:-1])  # 必须强转
            y.append(d[-1].decode())
    return np.round(X,2),y
def algorithmSelect(name):
    if name=='IF':
        #效果奇差
        return IsolationForest()
    elif name=='RF':
        return RandomForestClassifier(140)
    elif name == 'NB':
        return MultinomialNB()
def __calc_shannon_ent(category_list):
  """
  :param category_list: 类别列表
  :return: 该类别列表的熵值
  """
  label_count = {} # 统计数据集中每个类别的个数
  num = len(category_list) # 数据集个数
  for i in range(num):
    try:
      label_count[category_list[i]] += 1
    except KeyError:
      label_count[category_list[i]] = 1
  shannon_ent = 0.
  for k in label_count:
    prob = float(label_count[k]) / num
    shannon_ent -= prob * np.log2(prob) # 计算信息熵
  return shannon_ent
def __split_data(feature_matrix, category_list, feature_index, value):
  """
  筛选出指定特征值所对应的类别列表
  :param category_list: 类别列表
  :param feature_matrix: 特征矩阵
  :param feature_index: 指定特征索引
  :param value: 指定特征属性的特征值
  :return: 符合指定特征属性的特征值的类别列表
  """
  # feature_matrix = np.array(feature_matrix)
  ret_index = np.where(feature_matrix[:, feature_index] == value)[0] # 获取符合指定特征值的索引
  ret_category_list = [category_list[i] for i in ret_index] # 根据索引取得指定的所属类别，构建为列表
  return ret_category_list
def _choose_first_feature(feature_matrix, category_list):
  """
  根据信息增益获取最优特征
  :param feature_matrix: 特征矩阵
  :param category_list: 类别列表
  :return: 最优特征对应的索引
  """
  feature_num = len(feature_matrix[0]) # 特征个数
  data_num = len(category_list) # 数据集的个数
  base_shannon_ent = __calc_shannon_ent(category_list=category_list) # 原始数据的信息熵
  best_info_gain = 0 # 最优信息增益
  best_feature_index = -1 # 最优特征对应的索引
  for f in range(feature_num):

      uni_value_list = set(feature_matrix[:, f]) # 该特征属性所包含的特征值
      new_shannon_ent = 0.
      for value in uni_value_list:
          sub_cate_list = __split_data(feature_matrix=feature_matrix, category_list=category_list, feature_index=f, value=value)
          prob = float(len(sub_cate_list)) / data_num
          new_shannon_ent += prob * __calc_shannon_ent(sub_cate_list)
      info_gain = base_shannon_ent - new_shannon_ent # 信息增益
      # print('初始信息熵为：', base_shannon_ent, '按照特征%i分类后的信息熵为：' % f, new_shannon_ent, '信息增益为：', info_gain)
      if info_gain > best_info_gain:
          best_info_gain = info_gain
          best_feature_index = f
  return best_feature_index
def _choseFirstFeatureGini(X,Y):
    X = np.array(X, dtype='float64')
    Y = np.array(Y)
    numFeatures = len(X[0])
    numSimples = len(X)
    bestGini = 999999.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = X[:,i]
        uniqueVals = np.unique(featList)
        gini = 0.0
        for value in uniqueVals:
            indics = np.where(featList==value)
            subY = Y[indics]
            prob = len(subY)/float(numSimples)
            subProb = len(np.where(subY=='Y'))/float(len(subY))
            # gini += prob * (1.0 - pow(subProb, 2) - pow(1 - subProb, 2))
            gini += prob*2*subProb*(1-subProb)
        gini*=len(uniqueVals)
        # print(i,gini)
        if (gini < bestGini):
            bestGini = gini
            bestFeature = i
    return bestFeature
def splitX(X,indics):
    chose_ind = X[:,indics]
    return chose_ind
    # print(chose_ind)
    # remain_ind = X-chose_ind # error
    #
    # print(remain_ind)

def attrsSelect(X,y,algorithm,m,n):
    X = np.array(X, dtype='float64')
    fea_num = len(X[0])
    print("特征数：",fea_num)
    res = []
    # trainX, testX, trainY, testY = train_test_split(X, y, test_size=1./n)
    for loop_m in range(m):
        begin_time = time.time()
        chose_features = []
        chose_features.append(_choseFirstFeatureGini(X,y))
        # scaler = Normalizer()
        tmpX = splitX(X,chose_features)
        base_aux = bulidClassifier(tmpX,y,algorithm,n)
        best_aux = base_aux
        # print("%s\t%s"%(best_aux,chose_features))
        for m_i in range(m): # break m 次 ，确保没有特征增加
            #print(m_i,end='\t')
            while len(chose_features)<fea_num:
                tmp_chose_features = chose_features.copy()
                # print("当前特征：",tmp_chose_features)
                tmp_auxs = []
                tmp_indics = []
                for i in range(fea_num):
                    if i in chose_features:
                        continue
                    tmp_chose_features.append(i)
                    tmpX = splitX(X, tmp_chose_features)
                    ttmmpp_aux = bulidClassifier(tmpX,y,algorithm,n)
                    tmp_chose_features.remove(i)
                    # print(ttmmpp_aux)
                    if ttmmpp_aux-best_aux>0.:# ---TODO
                        tmp_auxs.append(ttmmpp_aux)
                        tmp_indics.append(i)
                if len(tmp_auxs)==0:
                    break
                max_auc = max(tmp_auxs)
                max_i = tmp_auxs.index(max_auc)
                real_i = tmp_indics[max_i]
                chose_features.append(real_i)
                #print("%s\t%s"%(max_auc,chose_features))
                best_aux = max_auc
        end_time = time.time()
        print("loop:%s\tauc:%s\tfeatures:%s\tuse_time:%s" % (loop_m,best_aux, chose_features,end_time-begin_time))
        res.append("%s\t%s\t%s\t%s\n"%(loop_m,best_aux, chose_features,end_time-begin_time))
    return res

def bf_attrs_select(X,y,algorithm,m,n):
    X = np.array(X, dtype='float64')
    fea_num = len(X[0])
    print("特征数：", fea_num)
    # trainX, testX, trainY, testY = train_test_split(X, y, test_size=1./n)
    for loop_m in range(m):
        begin_time = time.time()
        chose_features = [f_i for f_i in range(fea_num)]
        tmpX = splitX(X, chose_features)
        base_aux = bulidClassifier(tmpX, y, algorithm, n)
        best_aux = base_aux
        print("all features :%s\t%s"%(best_aux,chose_features))
        for m_i in range(m):  # break m 次 ，确保没有特征减少
            # print(m_i,end='\t')
            while len(chose_features) > 0 :
                tmp_chose_features = chose_features[:]
                # print("当前特征：",tmp_chose_features)
                tmp_auxs = []
                tmp_indics = []
                for i in chose_features:
                    tmp_chose_features.remove(i)
                    tmpX = splitX(X, tmp_chose_features)
                    ttmmpp_aux = bulidClassifier(tmpX, y, algorithm, n)
                    tmp_chose_features.append(i)
                    # print(ttmmpp_aux)
                    if ttmmpp_aux - best_aux > 0.:  # ---TODO
                        tmp_auxs.append(ttmmpp_aux)
                        tmp_indics.append(i)
                if len(tmp_auxs) == 0:
                    # print("break")
                    break
                max_auc = max(tmp_auxs)
                max_i = tmp_auxs.index(max_auc)
                real_i = tmp_indics[max_i]
                chose_features.remove(real_i)
                # print("%s\t%s"%(max_auc,chose_features))
                best_aux = max_auc
        end_time = time.time()
        print("loop:%s\tauc:%s\tfeatures:%s\tuse_time:%s" % (loop_m, best_aux, chose_features, end_time - begin_time))






def bulidClassifier(X,y,algorithm,n):
    '''
    :param X:
    :param y:
    :param algorithm:
    :param n: n折交叉
    :return: 取n折后平均值
    '''
    # iforest = IsolationForest()
    X = np.array(X,dtype='float64')
    y = np.array(y)
    scaler = Normalizer()
    # trainX,testX,trainY,testY = train_test_split(X,y,test_size=0.2)
    cv = KFold(n)
    roc_auc_s = []
    for i, (train, test) in enumerate(cv.split(X, y)):
        trainX = X[train]
        testX = X[test]
        trainY = y[train]
        testY = y[test]
        if len(np.unique(testY))==1 or len(np.unique(trainY))==1:
            continue
        trainX = scaler.fit_transform(trainX)
        testX = scaler.fit_transform(testX)
        algorithm.fit(trainX,trainY)
        pred = algorithm.predict_proba(testX)
        fpr, tpr, thresholds = roc_curve(testY, pred[:,1], pos_label='Y')
        roc_auc = auc(fpr,tpr)
        roc_auc_s.append(roc_auc)
    # print(roc_auc_s)
    return np.mean(np.array(roc_auc_s))
def bulidIF(X,y):
    algorithm = IsolationForest()
    X = np.array(X,dtype='float64')
    scaler = Normalizer()
    trainX,testX,trainY,testY = train_test_split(X,y,test_size=0.2)
    trainX = scaler.fit_transform(trainX)
    testX = scaler.fit_transform(testX)

    algorithm.fit(trainX,trainY)

    pred = algorithm.predict(testX)
    # print(pred,testY)
    fpr, tpr, thresholds = roc_curve(testY, pred, pos_label='N')
    roc_auc = auc(fpr,tpr)
    print(roc_auc)
    return roc_auc
def attrsAnalys(X):
    X = np.array(X)
    num = len(X[0])
    print("样本数目：",len(X))
    print("特征数目：",num)
    for i in range(num):
        i_feature = X[:,i]
        print("%s 号特征，取值个数  %s"%(i,len(np.unique(i_feature))))
if __name__ == '__main__':
    # PATH = '../NASADefectDataset/CleanedData/MDP/D\'\'/CM1.arff'
    # X,Y = processData(PATH)
    ######################################################################
    # with open('./Result/7-11.txt','w') as fw:
    #     for i in range(9,150):
    #         print(i,end='\t')
    #         ra1 = bulidClassifier(X,Y,RandomForestClassifier(i))
    #         ra2 = bulidClassifier(X,Y,MultinomialNB(i))
    #         ra3 = bulidIF(X,Y)
    #         fw.write(str(i)+'\t'+str(ra1)+'\t'+str(ra2)+'\t'+str(ra3)+'\n')
    #######################################################################
    # X2, Y2 = getOriData(PATH) # 没差别
    # print(X[0],X2[0])
    # print(_choose_first_feature(np.array(X),Y))
    ######################################################################
    # attrsAnalys(X)
    # print(_choseFirstFeatureGini(X,Y))

    # attrsSelect(X,Y,RandomForestClassifier(120),10,10)
    # bf_attrs_select(X,Y,RandomForestClassifier(120),10,10)
    # for i in range(5,26):
    #     print(bulidClassifier(X,Y,RandomForestClassifier(120),20)) #10
    #########################################################################
    path = '../NASADefectDataset/CleanedData/MDP/D\'\'/'
    with open('./Result/7-17.txt','w') as fw:
        for file in os.listdir(path):
            print(file)
            X, Y = processData(path+file)
            res = attrsSelect(X,Y,RandomForestClassifier(120),10,10)
            fw.write(str(file)+'\n')
            fw.writelines(res)
