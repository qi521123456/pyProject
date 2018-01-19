import hashlib
import random
import requests
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
    # except Exception as e:
    #     print(e)
def getCountry(path):
    zh2en = {}
    zhs = []
    with open(path,'r') as fr:
        lines = fr.readlines()
        for line in lines:
            if line[0]=='.':
                tmp = line[1:].split('-')
                if len(tmp)==2:
                    q = tmp[0]
                    # print(q)
                    time.sleep(1)
                    zh2en[translate(q)] = q
                elif len(tmp)>2:
                    zhs.append('-'.join(tmp[:-1]))
    return  zh2en,zhs
def process():
    zh2en = {'伊拉克': 'iraq', '尼加拉瓜': 'nicaragua', '阿根廷': 'argentina', '吉尔吉斯斯坦': 'kyrgyzstan', '阿富汗': 'afghanistan',
     '巴拉圭': 'paraguay', '尼日尔': 'niger', 'gibrlatar': 'gibrlatar', '不丹': 'bhutan', '爱沙尼亚': 'estonia', '新加坡': 'singapore',
     '拉脱维亚': 'latvia', '葡萄牙': 'portugal', '瓷器': 'china', '巴勒斯坦': 'palestine', '赞比亚': 'zambia', '阿尔及利亚': 'algeria',
     '芬兰': 'finland', '委内瑞拉': 'venezuela', '巴巴多斯': 'barbados', '斐济': 'fiji', '乌拉圭': 'uruguay', '柬埔寨': 'cambodia',
     '阿鲁巴': 'aruba', '也门': 'yemen', '马耳他': 'malta', '希腊': 'greece', '克罗地亚': 'croatia', '摩洛哥': 'morocco',
     '马来西亚': 'malaysia', '莫桑比克': 'mozambique', '瑞典': 'sweden', '法国': 'france', '墨西哥': 'mexico', '英格兰': 'england',
     '保加利亚': 'bulgaria', '圭亚那': 'guyana', '南极洲': 'antarctica', '津巴布韦': 'zimbabwe', '乌兹别克斯坦': 'uzbekistan',
     '斯洛文尼亚': 'slovenia', '波兰': 'poland', '德国': 'germany', '黎巴嫩': 'lebanon', '瑞士': 'switzerland', '塞内加尔': 'senegal',
     '摩尔多瓦': 'moldova', '阿塞拜疆': 'azerbaijan', '伯利兹': 'belize', '马其顿': 'macedonia', '俄罗斯': 'russia', '乔丹': 'jordan',
     '贝宁': 'benin', '罗马尼亚': 'romania', '布隆迪': 'burundi', '洪都拉斯': 'honduras', '汤加': 'tonga', '叙利亚': 'syria',
     '斯威士兰': 'swaziland', '冰岛': 'iceland', '苏里南': 'suriname', '塞舌尔': 'seychelles', '以色列': 'israel', '塞浦路斯': 'cyprus',
     '卢旺达': 'rwanda', '越南': 'vietnam', '安哥拉': 'angola', '马达加斯加': 'madagascar', '哥伦比亚': 'colombia', '伊朗': 'iran',
     '埃及': 'egypt', '乌克兰': 'ukraine', '印度尼西亚': 'indonesia', '澳大利亚': 'australia', '匈牙利': 'hungary', '格鲁吉亚': 'georgia',
     '格林纳达': 'grenada', '科威特': 'kuwait', '塔吉克斯坦': 'tajikistan', '突尼斯': 'tunisia', '威尔士': 'wales', '印度': 'india',
     '爱尔兰': 'ireland', '多米尼加': 'dominica', '厄立特里亚': 'eritrea', '巴基斯坦': 'pakistan', '安道尔': 'andorra', '牙买加': 'jamaica',
     '巴拿马': 'panama', '意大利': 'italy', '荷兰': 'netherlands', '莱索托': 'lesotho', '马拉维': 'malawi', '缅甸': 'myanmar',
     '毛里求斯': 'mauritius', '秘鲁': 'peru', '乍得': 'chad', '加拿大': 'canada', '古巴': 'cuba', '万那杜': 'vanatu', '厄瓜多尔': 'ecuador',
     '科摩罗': 'comoros', '老挝': 'laos', '孟加拉国': 'bangladesh', '卢森堡': 'luxemburg', '奥地利': 'austria', '比利时': 'belgium',
     '帕劳': 'palau', '索马里': 'somalia', '文莱': 'brunei', '纳米比亚': 'namibia', '立陶宛': 'lithuania', '黑山': 'montenegro',
     '列支敦士登': 'liechtenstein', '阿尔巴尼亚': 'albania', '格陵兰岛': 'greenland', '泰国': 'thailand', '肯尼亚': 'kenya',
     '尼泊尔': 'nepal', '瑙鲁': 'nauru', '阿曼': 'oman', '马尔代夫': 'maldives', '几内亚': 'guinea', '卡塔尔': 'quatar',
     '埃塞俄比亚': 'ethiopia', '加纳': 'ghana', '加泰罗尼亚': 'catalonia', '苏格兰': 'scotland', '火鸡': 'turkey', '白俄罗斯': 'belarus',
     '蒙古': 'mongolia', '摩纳哥': 'monaco', '喀麦隆': 'cameroon', '瓜地马拉': 'guatemala', '利比里亚': 'liberia', '坦桑尼亚': 'tanzania',
     '马里': 'mali', '西班牙': 'spain', '加蓬': 'gabon', '博茨瓦纳': 'botswana', '吉布提': 'djibouti', '毛里塔尼亚': 'mauritania',
     '巴西': 'brazil', '菲律宾': 'philippines', '土库曼斯坦': 'turkmenistan', '乌干达': 'uganda', '丹麦': 'denmark', '苏丹': 'sudan',
     '智利': 'chile', '萨摩亚': 'samoa', '巴林': 'bahrain', '澳门': 'macau', '尼日利亚': 'nigeria', '亚美尼亚': 'armenia',
     '密克罗尼西亚': 'micronesia', '基里巴斯': 'kiribati', '塞尔维亚': 'serbia', '海地': 'haiti', '哈萨克斯坦': 'kazakhstan', '日本': 'japan',
     '图瓦卢': 'tuvalu', '玻利维亚': 'bolivia', '布基纳': 'burkina', '斯洛伐克': 'slovakia', '挪威': 'norway', '利比亚': 'lybia',
     '多哥': 'togo'}

    zhs = ['antigua-and-barbuda', 'the-bahamas', 'bosnia-and-herzegovina', 'cape-verde', 'central-african-republic',
     'democratic-republic-of-the-congo', 'republic-of-the-congo', 'costa-rica', 'cote-divoire', 'czech-republic',
     'domnican-republic', 'el-salvador', 'equatorial-guinea', 'european-union', 'faroe-islnads', 'the-gambia',
     'guinea-bissau', 'hong-kong', 'north-korea', 'south-korea', 'marshall-islands', 'new-zealand', 'northern-ireland',
     'papua-new-guinea', 'puerto-rico', 'saint-kitts-and-nevis', 'saint-lucia', 'saint-vincent-and-the-grenadines',
     'san-marino', 'sao-tome-and-principe', 'saudi-arabia', 'sierra-leone', 'solomon-islands', 'south-africa',
     'sri-lanka', 'timor-leste', 'trinidad-and-tobago', 'united-arab-emirates', 'united-kingdom',
     'united-states-of-america', 'vatican-city', 'western-sahara']
    for i in zhs:
        zh2en[translate(i)] = i
        time.sleep(1)
    print(zh2en)
if __name__ == '__main__':
    process()