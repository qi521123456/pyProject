import time,os
from scipy.io import arff
import numpy as np
def _getOriDataAttr(path):
    with open(path, 'r') as fr:
        data, meta = arff.loadarff(fr)
    return meta
def _iniRes():
    path = '../NASADefectDataset/CleanedData/MDP/D\'\'/'
    initRes = {}
    for f in os.listdir(path):
        meta = _getOriDataAttr(path + f)
        dataname = meta.name
        initRes[dataname] = {'attr_num':len(meta.names()) - 1}
    print(initRes)


def report17(path='/home/mannix/Documents/thesis/特征优化方案/NovP2/7-17.txt'):
    names = []
    result = {'PC4': {'attr_num': 37}, 'KC1': {'attr_num': 21}, 'MC2': {'attr_num': 39}, 'CM1': {'attr_num': 37},
              'PC2': {'attr_num': 36}, 'JM1': {'attr_num': 21}, 'PC3': {'attr_num': 37}, 'MC1': {'attr_num': 38},
              'KC3': {'attr_num': 39}, 'MW1': {'attr_num': 37}, 'PC5': {'attr_num': 38}, 'PC1': {'attr_num': 37}}
    with open(path,'r') as fr:
        name = ''
        tmpaucs = []
        tmpfeas = []
        tmptimes = []
        tmpfealen = []
        for line in fr:
            tmpline = line.split('\t')
            if len(tmpline) == 1:
                if len(names) > 0: # 存上个name的数据
                    result[name]['auc'] = tmpaucs
                    result[name]['fea'] = tmpfeas
                    result[name]['time'] = tmptimes
                    result[name]['fea_len'] = tmpfealen
                name = tmpline[0].split('.')[0]
                names.append(name)
                tmpaucs = []
                tmpfeas = []
                tmptimes = []
                tmpfealen = []
            else:
                tmpaucs.append(eval(tmpline[1]))
                tmpfeas.append(eval(tmpline[2]))
                tmptimes.append(eval(tmpline[3]))
                tmpfealen.append(len(eval(tmpline[2])))
        # 最后一个
        result[name]['auc'] = tmpaucs
        result[name]['fea'] = tmpfeas
        result[name]['time'] = tmptimes
        result[name]['fea_len'] = tmpfealen
    return names,result

def report18(path='/home/mannix/Documents/thesis/特征优化方案/NovP2/7-18.txt'):
    names = []
    result = {'PC4': {'attr_num': 37}, 'KC1': {'attr_num': 21}, 'MC2': {'attr_num': 39}, 'CM1': {'attr_num': 37},
              'PC2': {'attr_num': 36}, 'JM1': {'attr_num': 21}, 'PC3': {'attr_num': 37}, 'MC1': {'attr_num': 38},
              'KC3': {'attr_num': 39}, 'MW1': {'attr_num': 37}, 'PC5': {'attr_num': 38}, 'PC1': {'attr_num': 37}}
    with open(path,'r') as fr:
        name = ''
        tmpaucs = []
        tmpfeas = []
        tmptimes = []
        tmpallaucs = []
        tmpfealen = []
        for line in fr:
            tmpline = line.split('\t')
            if len(tmpline) == 1:
                if len(names) > 0: # 存上个name的数据
                    result[name]['auc'] = tmpaucs
                    result[name]['fea'] = tmpfeas
                    result[name]['time'] = tmptimes
                    result[name]['all_auc'] = tmpallaucs
                    result[name]['fea_len'] = tmpfealen
                name = tmpline[0].split('.')[0]
                names.append(name)
                tmpaucs = []
                tmpfeas = []
                tmptimes = []
                tmpallaucs = []
                tmpfealen = []
            else:
                tmpallaucs.append(eval(tmpline[1]))
                tmpaucs.append(eval(tmpline[2]))
                tmpfeas.append(eval(tmpline[3]))
                tmptimes.append(eval(tmpline[4]))
                tmpfealen.append(len(eval(tmpline[3])))
        # 最后一个
        result[name]['auc'] = tmpaucs
        result[name]['fea'] = tmpfeas
        result[name]['time'] = tmptimes
        result[name]['all_auc'] = tmpallaucs
        result[name]['fea_len'] = tmpfealen
    return names, result

def feaNum():
    names,fs = report17()
    _,be = report18()
    print("%s\t%s\t%s\t%s" % ('数据集', '全部', '向前搜索', '向后搜索'))
    for name in names:
        attrNum = fs[name]['attr_num']
        fsFeaNum = np.rint(np.mean(fs[name]['fea_len']))
        beFeaNum = np.rint(np.mean(be[name]['fea_len']))
        print("%s\t%d\t%d\t%d"%(name,attrNum,fsFeaNum,beFeaNum))

def useTime():
    names, fs = report17()
    _, be = report18()
    print("%s\t%s\t%s" % ('', '向前搜索', '向后搜索'))
    for name in names:
        fsTime = np.mean(fs[name]['time'])
        beTime = np.mean(be[name]['time'])
        print("%s\t%s\t%s" % (name, fsTime,beTime))
if __name__ == '__main__':
    useTime()