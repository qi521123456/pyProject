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
        initRes[dataname] = meta.names()[:-1]  #{'attr_num':len(meta.names()) - 1}
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

def standdev():
    names, fs = report17()
    _, be = report18()
    print("%s\t%s\t%s\t%s" % (' ', '全部', '向前搜索', '向后搜索'))
    for name in names:
        stdall = np.std(be[name]['all_auc'])
        stdfs = np.std(fs[name]['auc'])
        stdbe = np.std(be[name]['auc'])
        print("%s\t%s\t%s\t%s"%(name,stdall,stdfs,stdbe))

def stdfeaNum():
    names, fs = report17()
    _, be = report18()
    print("%s\t%s\t%s" % (' ', '向前搜索', '向后搜索'))
    for name in names:
        stdfs = min(fs[name]['fea_len'])
        stdbe = min(be[name]['fea_len'])
        print("%s\t%s\t%s" % (name, stdfs, stdbe))

def feaUse(threshold=5):
    feas = {'PC4': ['LOC_BLANK', 'BRANCH_COUNT', 'CALL_PAIRS', 'LOC_CODE_AND_COMMENT', 'LOC_COMMENTS', 'CONDITION_COUNT',
                    'CYCLOMATIC_COMPLEXITY', 'CYCLOMATIC_DENSITY', 'DECISION_COUNT', 'DECISION_DENSITY',
                    'DESIGN_COMPLEXITY', 'DESIGN_DENSITY', 'EDGE_COUNT', 'ESSENTIAL_COMPLEXITY', 'ESSENTIAL_DENSITY',
                    'LOC_EXECUTABLE', 'PARAMETER_COUNT', 'HALSTEAD_CONTENT', 'HALSTEAD_DIFFICULTY', 'HALSTEAD_EFFORT',
                    'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH', 'HALSTEAD_LEVEL', 'HALSTEAD_PROG_TIME', 'HALSTEAD_VOLUME',
                    'MAINTENANCE_SEVERITY', 'MODIFIED_CONDITION_COUNT', 'MULTIPLE_CONDITION_COUNT', 'NODE_COUNT',
                    'NORMALIZED_CYLOMATIC_COMPLEXITY', 'NUM_OPERANDS', 'NUM_OPERATORS', 'NUM_UNIQUE_OPERANDS',
                    'NUM_UNIQUE_OPERATORS', 'NUMBER_OF_LINES', 'PERCENT_COMMENTS', 'LOC_TOTAL'],
            'KC1': ['LOC_BLANK', 'BRANCH_COUNT', 'LOC_CODE_AND_COMMENT', 'LOC_COMMENTS', 'CYCLOMATIC_COMPLEXITY',
                    'DESIGN_COMPLEXITY', 'ESSENTIAL_COMPLEXITY', 'LOC_EXECUTABLE', 'HALSTEAD_CONTENT',
                    'HALSTEAD_DIFFICULTY', 'HALSTEAD_EFFORT', 'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH',
                    'HALSTEAD_LEVEL', 'HALSTEAD_PROG_TIME', 'HALSTEAD_VOLUME', 'NUM_OPERANDS', 'NUM_OPERATORS',
                    'NUM_UNIQUE_OPERANDS', 'NUM_UNIQUE_OPERATORS', 'LOC_TOTAL'],
            'MC2': ['LOC_BLANK', 'BRANCH_COUNT', 'CALL_PAIRS', 'LOC_CODE_AND_COMMENT', 'LOC_COMMENTS', 'CONDITION_COUNT', 'CYCLOMATIC_COMPLEXITY', 'CYCLOMATIC_DENSITY', 'DECISION_COUNT', 'DECISION_DENSITY', 'DESIGN_COMPLEXITY', 'DESIGN_DENSITY', 'EDGE_COUNT', 'ESSENTIAL_COMPLEXITY', 'ESSENTIAL_DENSITY', 'LOC_EXECUTABLE', 'PARAMETER_COUNT', 'GLOBAL_DATA_COMPLEXITY', 'GLOBAL_DATA_DENSITY', 'HALSTEAD_CONTENT', 'HALSTEAD_DIFFICULTY', 'HALSTEAD_EFFORT', 'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH', 'HALSTEAD_LEVEL', 'HALSTEAD_PROG_TIME', 'HALSTEAD_VOLUME', 'MAINTENANCE_SEVERITY', 'MODIFIED_CONDITION_COUNT', 'MULTIPLE_CONDITION_COUNT', 'NODE_COUNT', 'NORMALIZED_CYLOMATIC_COMPLEXITY', 'NUM_OPERANDS', 'NUM_OPERATORS', 'NUM_UNIQUE_OPERANDS', 'NUM_UNIQUE_OPERATORS', 'NUMBER_OF_LINES', 'PERCENT_COMMENTS', 'LOC_TOTAL'], 'CM1': ['LOC_BLANK', 'BRANCH_COUNT', 'CALL_PAIRS', 'LOC_CODE_AND_COMMENT', 'LOC_COMMENTS', 'CONDITION_COUNT', 'CYCLOMATIC_COMPLEXITY', 'CYCLOMATIC_DENSITY', 'DECISION_COUNT', 'DECISION_DENSITY', 'DESIGN_COMPLEXITY', 'DESIGN_DENSITY', 'EDGE_COUNT', 'ESSENTIAL_COMPLEXITY', 'ESSENTIAL_DENSITY', 'LOC_EXECUTABLE', 'PARAMETER_COUNT', 'HALSTEAD_CONTENT', 'HALSTEAD_DIFFICULTY', 'HALSTEAD_EFFORT', 'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH', 'HALSTEAD_LEVEL', 'HALSTEAD_PROG_TIME', 'HALSTEAD_VOLUME', 'MAINTENANCE_SEVERITY', 'MODIFIED_CONDITION_COUNT', 'MULTIPLE_CONDITION_COUNT', 'NODE_COUNT', 'NORMALIZED_CYLOMATIC_COMPLEXITY', 'NUM_OPERANDS', 'NUM_OPERATORS', 'NUM_UNIQUE_OPERANDS', 'NUM_UNIQUE_OPERATORS', 'NUMBER_OF_LINES', 'PERCENT_COMMENTS', 'LOC_TOTAL'], 'PC2': ['BRANCH_COUNT', 'CALL_PAIRS', 'LOC_CODE_AND_COMMENT', 'LOC_COMMENTS', 'CONDITION_COUNT', 'CYCLOMATIC_COMPLEXITY', 'CYCLOMATIC_DENSITY', 'DECISION_COUNT', 'DECISION_DENSITY', 'DESIGN_COMPLEXITY', 'DESIGN_DENSITY', 'EDGE_COUNT', 'ESSENTIAL_COMPLEXITY', 'ESSENTIAL_DENSITY', 'LOC_EXECUTABLE', 'PARAMETER_COUNT', 'HALSTEAD_CONTENT', 'HALSTEAD_DIFFICULTY', 'HALSTEAD_EFFORT', 'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH', 'HALSTEAD_LEVEL', 'HALSTEAD_PROG_TIME', 'HALSTEAD_VOLUME', 'MAINTENANCE_SEVERITY', 'MODIFIED_CONDITION_COUNT', 'MULTIPLE_CONDITION_COUNT', 'NODE_COUNT', 'NORMALIZED_CYLOMATIC_COMPLEXITY', 'NUM_OPERANDS', 'NUM_OPERATORS', 'NUM_UNIQUE_OPERANDS', 'NUM_UNIQUE_OPERATORS', 'NUMBER_OF_LINES', 'PERCENT_COMMENTS', 'LOC_TOTAL'], 'JM1': ['LOC_BLANK', 'BRANCH_COUNT', 'LOC_CODE_AND_COMMENT', 'LOC_COMMENTS', 'CYCLOMATIC_COMPLEXITY', 'DESIGN_COMPLEXITY', 'ESSENTIAL_COMPLEXITY', 'LOC_EXECUTABLE', 'HALSTEAD_CONTENT', 'HALSTEAD_DIFFICULTY', 'HALSTEAD_EFFORT', 'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH', 'HALSTEAD_LEVEL', 'HALSTEAD_PROG_TIME', 'HALSTEAD_VOLUME', 'NUM_OPERANDS', 'NUM_OPERATORS', 'NUM_UNIQUE_OPERANDS', 'NUM_UNIQUE_OPERATORS', 'LOC_TOTAL'], 'PC3': ['LOC_BLANK', 'BRANCH_COUNT', 'CALL_PAIRS', 'LOC_CODE_AND_COMMENT', 'LOC_COMMENTS', 'CONDITION_COUNT', 'CYCLOMATIC_COMPLEXITY', 'CYCLOMATIC_DENSITY', 'DECISION_COUNT', 'DECISION_DENSITY', 'DESIGN_COMPLEXITY', 'DESIGN_DENSITY', 'EDGE_COUNT', 'ESSENTIAL_COMPLEXITY', 'ESSENTIAL_DENSITY', 'LOC_EXECUTABLE', 'PARAMETER_COUNT', 'HALSTEAD_CONTENT', 'HALSTEAD_DIFFICULTY', 'HALSTEAD_EFFORT', 'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH', 'HALSTEAD_LEVEL', 'HALSTEAD_PROG_TIME', 'HALSTEAD_VOLUME', 'MAINTENANCE_SEVERITY', 'MODIFIED_CONDITION_COUNT', 'MULTIPLE_CONDITION_COUNT', 'NODE_COUNT', 'NORMALIZED_CYLOMATIC_COMPLEXITY', 'NUM_OPERANDS', 'NUM_OPERATORS', 'NUM_UNIQUE_OPERANDS', 'NUM_UNIQUE_OPERATORS', 'NUMBER_OF_LINES', 'PERCENT_COMMENTS', 'LOC_TOTAL'], 'MC1': ['LOC_BLANK', 'BRANCH_COUNT', 'CALL_PAIRS', 'LOC_CODE_AND_COMMENT', 'LOC_COMMENTS', 'CONDITION_COUNT', 'CYCLOMATIC_COMPLEXITY', 'CYCLOMATIC_DENSITY', 'DECISION_COUNT', 'DESIGN_COMPLEXITY', 'DESIGN_DENSITY', 'EDGE_COUNT', 'ESSENTIAL_COMPLEXITY', 'ESSENTIAL_DENSITY', 'LOC_EXECUTABLE', 'PARAMETER_COUNT', 'GLOBAL_DATA_COMPLEXITY', 'GLOBAL_DATA_DENSITY', 'HALSTEAD_CONTENT', 'HALSTEAD_DIFFICULTY', 'HALSTEAD_EFFORT', 'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH', 'HALSTEAD_LEVEL', 'HALSTEAD_PROG_TIME', 'HALSTEAD_VOLUME', 'MAINTENANCE_SEVERITY', 'MODIFIED_CONDITION_COUNT', 'MULTIPLE_CONDITION_COUNT', 'NODE_COUNT', 'NORMALIZED_CYLOMATIC_COMPLEXITY', 'NUM_OPERANDS', 'NUM_OPERATORS', 'NUM_UNIQUE_OPERANDS', 'NUM_UNIQUE_OPERATORS', 'NUMBER_OF_LINES', 'PERCENT_COMMENTS', 'LOC_TOTAL'], 'KC3': ['LOC_BLANK', 'BRANCH_COUNT', 'CALL_PAIRS', 'LOC_CODE_AND_COMMENT', 'LOC_COMMENTS', 'CONDITION_COUNT', 'CYCLOMATIC_COMPLEXITY', 'CYCLOMATIC_DENSITY', 'DECISION_COUNT', 'DECISION_DENSITY', 'DESIGN_COMPLEXITY', 'DESIGN_DENSITY', 'EDGE_COUNT', 'ESSENTIAL_COMPLEXITY', 'ESSENTIAL_DENSITY', 'LOC_EXECUTABLE', 'PARAMETER_COUNT', 'GLOBAL_DATA_COMPLEXITY', 'GLOBAL_DATA_DENSITY', 'HALSTEAD_CONTENT', 'HALSTEAD_DIFFICULTY', 'HALSTEAD_EFFORT', 'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH', 'HALSTEAD_LEVEL', 'HALSTEAD_PROG_TIME', 'HALSTEAD_VOLUME', 'MAINTENANCE_SEVERITY', 'MODIFIED_CONDITION_COUNT', 'MULTIPLE_CONDITION_COUNT', 'NODE_COUNT', 'NORMALIZED_CYLOMATIC_COMPLEXITY', 'NUM_OPERANDS', 'NUM_OPERATORS', 'NUM_UNIQUE_OPERANDS', 'NUM_UNIQUE_OPERATORS', 'NUMBER_OF_LINES', 'PERCENT_COMMENTS', 'LOC_TOTAL'], 'MW1': ['LOC_BLANK', 'BRANCH_COUNT', 'CALL_PAIRS', 'LOC_CODE_AND_COMMENT', 'LOC_COMMENTS', 'CONDITION_COUNT', 'CYCLOMATIC_COMPLEXITY', 'CYCLOMATIC_DENSITY', 'DECISION_COUNT', 'DECISION_DENSITY', 'DESIGN_COMPLEXITY', 'DESIGN_DENSITY', 'EDGE_COUNT', 'ESSENTIAL_COMPLEXITY', 'ESSENTIAL_DENSITY', 'LOC_EXECUTABLE', 'PARAMETER_COUNT', 'HALSTEAD_CONTENT', 'HALSTEAD_DIFFICULTY', 'HALSTEAD_EFFORT', 'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH', 'HALSTEAD_LEVEL', 'HALSTEAD_PROG_TIME', 'HALSTEAD_VOLUME', 'MAINTENANCE_SEVERITY', 'MODIFIED_CONDITION_COUNT', 'MULTIPLE_CONDITION_COUNT', 'NODE_COUNT', 'NORMALIZED_CYLOMATIC_COMPLEXITY', 'NUM_OPERANDS', 'NUM_OPERATORS', 'NUM_UNIQUE_OPERANDS', 'NUM_UNIQUE_OPERATORS', 'NUMBER_OF_LINES', 'PERCENT_COMMENTS', 'LOC_TOTAL'], 'PC5': ['LOC_BLANK', 'BRANCH_COUNT', 'CALL_PAIRS', 'LOC_CODE_AND_COMMENT', 'LOC_COMMENTS', 'CONDITION_COUNT', 'CYCLOMATIC_COMPLEXITY', 'CYCLOMATIC_DENSITY', 'DECISION_COUNT', 'DESIGN_COMPLEXITY', 'DESIGN_DENSITY', 'EDGE_COUNT', 'ESSENTIAL_COMPLEXITY', 'ESSENTIAL_DENSITY', 'LOC_EXECUTABLE', 'PARAMETER_COUNT', 'GLOBAL_DATA_COMPLEXITY', 'GLOBAL_DATA_DENSITY', 'HALSTEAD_CONTENT', 'HALSTEAD_DIFFICULTY', 'HALSTEAD_EFFORT', 'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH', 'HALSTEAD_LEVEL', 'HALSTEAD_PROG_TIME', 'HALSTEAD_VOLUME', 'MAINTENANCE_SEVERITY', 'MODIFIED_CONDITION_COUNT', 'MULTIPLE_CONDITION_COUNT', 'NODE_COUNT', 'NORMALIZED_CYLOMATIC_COMPLEXITY', 'NUM_OPERANDS', 'NUM_OPERATORS', 'NUM_UNIQUE_OPERANDS', 'NUM_UNIQUE_OPERATORS', 'NUMBER_OF_LINES', 'PERCENT_COMMENTS', 'LOC_TOTAL'], 'PC1': ['LOC_BLANK', 'BRANCH_COUNT', 'CALL_PAIRS', 'LOC_CODE_AND_COMMENT', 'LOC_COMMENTS', 'CONDITION_COUNT', 'CYCLOMATIC_COMPLEXITY', 'CYCLOMATIC_DENSITY', 'DECISION_COUNT', 'DECISION_DENSITY', 'DESIGN_COMPLEXITY', 'DESIGN_DENSITY', 'EDGE_COUNT', 'ESSENTIAL_COMPLEXITY', 'ESSENTIAL_DENSITY', 'LOC_EXECUTABLE', 'PARAMETER_COUNT', 'HALSTEAD_CONTENT', 'HALSTEAD_DIFFICULTY', 'HALSTEAD_EFFORT', 'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH', 'HALSTEAD_LEVEL', 'HALSTEAD_PROG_TIME', 'HALSTEAD_VOLUME', 'MAINTENANCE_SEVERITY', 'MODIFIED_CONDITION_COUNT', 'MULTIPLE_CONDITION_COUNT', 'NODE_COUNT', 'NORMALIZED_CYLOMATIC_COMPLEXITY', 'NUM_OPERANDS', 'NUM_OPERATORS', 'NUM_UNIQUE_OPERANDS', 'NUM_UNIQUE_OPERATORS', 'NUMBER_OF_LINES', 'PERCENT_COMMENTS', 'LOC_TOTAL']}
    names, fs = report17()
    subfeas = {}
    unifeas = set()
    for i,name in enumerate(names):
        #####################
        # 取交集
        # fea = set()
        # for i,feai in enumerate(fs[name]['fea']):
        #     if i==0:
        #         fea = set(feai)
        #     else:
        #         fea = fea.intersection(set(feai))
        # print(name,fea)
        #######################

        feanum = list(np.zeros(len(feas[name])))
        for feai in fs[name]['fea']:
            for i in feai:
                feanum[i]+=1
        feaindex = np.where(np.array(feanum)>threshold)[0].tolist()
        fea = np.array(feas[name])[feaindex].tolist()
        subfea = {'all_len':len(feas[name]),'sub_len':len(fea),'fea':fea}
        subfeas[name]=subfea
        if i==0:
            unifeas = set(fea)
        else:
            unifeas = unifeas.union(set(fea))
    unifeas = list(unifeas)
    subfeanum = {}
    for i in unifeas:
        subfeanum[i]=0
    for name in names:
        for j in subfeas[name]['fea']:
            subfeanum[j]+=1
    d = subfeanum
    print(sorted(d.items(), key=lambda d:d[1]))
    # print("%s&%s & %s & %s"%('','特征子集','子集特征数量','原特征数量'))
    # for name in names:
    #     print("%s & %s & %s & %s"%(name,' '.join(sorted(subfeas[name]['fea'])),subfeas[name]['sub_len'],subfeas[name]['all_len']))

if __name__ == '__main__':
    feaUse()