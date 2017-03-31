
import requests,re
import execjs

segment_flag = "segment_flag."
ctx = execjs.compile("""
   function TL(a) {
   var k = "";
   var b = 406644;
   var b1 = 3293161072;

   var jd = ".";
   var $b = "+-a^+6";
   var Zb = "+-3^+b+-f";

   for (var e = [], f = 0, g = 0; g < a.length; g++) {
       var m = a.charCodeAt(g);
       128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
       e[f++] = m >> 18 | 240,
       e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
       e[f++] = m >> 6 & 63 | 128),
       e[f++] = m & 63 | 128)
   }
   a = b;
   for (f = 0; f < e.length; f++) a += e[f],
   a = RL(a, $b);
   a = RL(a, Zb);
   a ^= b1 || 0;
   0 > a && (a = (a & 2147483647) + 2147483648);
   a %= 1E6;
   return a.toString() + jd + (a ^ b)
};

function RL(a, b) {
   var t = "a";
   var Yb = "+";
   for (var c = 0; c < b.length - 2; c += 3) {
       var d = b.charAt(c + 2),
       d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
       d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
       a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
   }
   return a
}
""")


def getTk(text):
    return ctx.call("TL", text)

def translate(english_text):
    tk = getTk(english_text)
    header = {
        'Host':'translate.google.cn',
        'User - Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept - Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept - Encoding": "gzip, deflate",
        "Cookie": "NID=98=fomehjNfQZevs2WFPU6S7IAvJSDRpfUyaLHl8YZ4aBk8jmwMDOS2XLq_lUASgDJe8dQHjSp2tK"
                "JCQrx1GUHmyFiNlmkI3I7bVqnyr-6cG1SM8zMKy27xfaPlxy-eH7CM; _ga=GA1.3.1223342825.1488333678",
        'Connection': "keep-alive",
        'Upgrade - Insecure - Requests': "1",
        'Cache - Control': "max-age=0"
        #'Refer':'http://translate.google.cn/#en/zh-CN/%s'%english_text
    }
    url = "http://translate.google.cn/translate_a/single?client=t&sl=en&tl=" \
          "zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=" \
          "ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=1&tk=%s&q=%s"%(tk,english_text)
    r = requests.get(url,headers=header)
    content = r.text.split('"')
    return content[1]

def get_txt(filename):
    segflag = segment_flag
    with open(filename,'r',encoding='utf-8') as fr:
        lines = []
        for line in fr.readlines():
            if line == '\n':
                lines.append(segflag)
                continue
            sl = line.strip()

            if sl[-1] == '-':
                sl = sl[:-1]
            lines.append(sl)
        context = ' '.join(lines)
        sentences = context.split('.')
    return sentences


def main(txt):
    segflag = segment_flag
    for sentence in txt[:-1]:
        res = translate(sentence)
        if res == segflag[:-1]:
            print('\n')
            continue
        print(res+'。',end=' ')



if __name__ == '__main__':
    r = get_txt("D:/test.txt")
    #print(segment_flag[:-1])
    main(r)
