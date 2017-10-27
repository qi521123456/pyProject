from bs4 import BeautifulSoup

def parsehtml(html):
    soup = BeautifulSoup(html)
    # print(soup.prettify()) # 排版好
    # print(soup.title,soup.head.meta) Tag ：name,attrs
    # print(soup.title.string) # NavigableString ,type(soup.a.string)==bs4.element.Comment
    # for i in soup.body.stripped_strings:
    #     print(i)

    for i in soup.head.children:
        if i.name=="meta":
            attr = i.attrs
            if attr.get('name') is not None:
                print(attr['name'],attr['content'])


if __name__ == '__main__':
    parsehtml(open("E:/t.html",encoding='utf8'))