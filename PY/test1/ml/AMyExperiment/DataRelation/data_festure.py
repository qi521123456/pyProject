import os
from scipy.io import arff
import hashlib
import random
import requests
import numpy as np
import time
def translate(q):
    appid = '20151113000005349'
    secretKey = 'osubCEzlGjzvw8qdQc41'
    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode())
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + q + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    # try:
    res = requests.get(myurl)
    txt = eval(res.text)
    print(txt)
    return txt['trans_result'][0]['dst']
def get_meta(path):
    data,meta = arff.loadarff(open(path,'r'))
    label = []
    for d in data:
        label.append(d[-1])
    return meta.names(),meta.types(),[len(data[0])-1,len(data),label.count(b'Y'),label.count(b'N'),round(label.count(b'Y')/len(data),3)]

name_list = ['NUM_UNIQUE_OPERATORS', 'HALSTEAD_ERROR_EST', 'HALSTEAD_LENGTH', 'BRANCH_COUNT', 'LOC_BLANK', 'HALSTEAD_CONTENT', 'MULTIPLE_CONDITION_COUNT', 'NUM_OPERATORS', 'NORMALIZED_CYLOMATIC_COMPLEXITY', 'HALSTEAD_PROG_TIME', 'PARAMETER_COUNT', 'MODIFIED_CONDITION_COUNT', 'LOC_TOTAL', 'NODE_COUNT', 'CONDITION_COUNT', 'NUM_OPERANDS', 'DESIGN_DENSITY', 'CYCLOMATIC_DENSITY', 'ESSENTIAL_DENSITY', 'DESIGN_COMPLEXITY', 'CALL_PAIRS', 'DECISION_DENSITY', 'NUM_UNIQUE_OPERANDS', 'GLOBAL_DATA_COMPLEXITY', 'HALSTEAD_DIFFICULTY', 'GLOBAL_DATA_DENSITY', 'CYCLOMATIC_COMPLEXITY', 'MAINTENANCE_SEVERITY', 'HALSTEAD_LEVEL', 'LOC_EXECUTABLE', 'LOC_CODE_AND_COMMENT', 'ESSENTIAL_COMPLEXITY', 'HALSTEAD_VOLUME', 'LOC_COMMENTS', 'PERCENT_COMMENTS', 'HALSTEAD_EFFORT', 'DECISION_COUNT', 'NUMBER_OF_LINES', 'EDGE_COUNT','PATHOLOGICAL_COMPLEXITY']
def main():
    PATH = '../NASADefectDataset/CleanedData/MDP/D\'\'/'
    # PATH = '../NASADefectDataset/OriginalData/MDP/'
    all_name = []
    print(name_list.__len__())
    data_map = {}
    all_info = []
    for file in os.listdir(PATH):
        if file == 'KC4.arff':
            continue
        print(file)
        names, types, data_info = get_meta(PATH + file)
        all_info.append(data_info)
        contain_name = []
        for i in names:
            try:
                indexnum = name_list.index(i)
                contain_name.append(indexnum)
            except Exception:
                contain_name.append(0)
        data_name = file.split('.')[0]
        all_name.append(data_name)
        data_map[data_name] = []
        for i in range(len(name_list)):
            if i in contain_name:
                data_map[data_name].append('√')
            else:
                data_map[data_name].append('×')
    info_name = ['属性数目', '样本数目', '正类数目', '负类数目', '正类占比']
    with open('/home/mannix/Documents/thesis/上采样方案/dataset\'\'.txt', 'w') as fw:
        fw.write('属性\t' + '\t'.join(all_name) + '\t\n')
        for i in range(len(name_list)):

            s = name_list[i]+'\t'
            for j in all_name:
                s += data_map[j][i] + '\t'
            s += '\n'
            fw.write(s)
        for i in range(len(info_name)):
            s = info_name[i] + '\t'
            for j in all_info:
                s += str(j[i]) + '\t'
            s += '\n'
            fw.write(s)


def main2():
    PATH = '../NASADefectDataset/CleanedData/MDP/D\'\'/CM1.arff'
    path2 = '../NASADefectDataset/OriginalData/MDP/'
    all_l = []
    for file in os.listdir(path2):
        if file == 'KC4.arff':
            continue
        print(file)
        names, types, data_info = get_meta(path2 + file)
        all_l.extend(names)
    nl1 = list(set(all_l))

if __name__ == '__main__':
    main()


