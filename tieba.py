
import tld as tld
import mysql.connector
import pymysql
import re
import time
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
conn=mysql.connector.connect(
user='root',
password='123456',
host='127.0.0.1',
port='3306',
database='test'
)

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}




def getASection(url, bookName):
    cursor = conn.cursor()
    try:
        bookName += ".txt"
        # f = open(bookName, "a", encoding='utf-8')  # 利用追加的方式打开文件，这样后面章节的内容不会覆盖前面章节
        rsp = requests.get(url, headers=headers)
        rsp.encoding = 'utf-8'
        bs = BeautifulSoup(rsp.text, 'html.parser')
        title = bs.select('h1')[0]
        # f.write(title.text)
        # f.write("\n")
        body = bs.select('div.TRS_Editor')[0]
        paragraphs = body.find_all('p')
        contents = []

        contents = paragraphs
        title = title
        content = str(body)[:]
        values = ('article_title', 'article_site','article_content','article_download_time')
        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        site = '百度贴吧'
        data = (title, site,content,times)
        query = "INSERT INTO yq_article(article_title,article_site,article_content,article_download_time) VALUES ('%s','%s','%s','%s')" % (data)
        try:
            cursor.execute(query)
            conn.commit()

        except Exception as err:
            print("sql语句执行错误", err)
            conn.rollback()
        cursor.close()
        # f.writelines(content)
        # f.close()
    except IndexError as e:
        print("======", e)


    finally:
        print('finally...')





def getBooks(url):

    bookUrls = dict()  # 用字典来存放小说信息，键为书名，值为链接地址
    rsp = requests.get(url, headers=headers)
    rsp.encoding = 'utf-8'
    bs = BeautifulSoup(rsp.text, 'html.parser')

    # try:
    bookList = bs.select('ul #thread_list')[0]
    sorts = bookList.select('a')
    # except Exception as err:
    #     print("======", err)
    for sort in sorts:
        book = sort.findNext('a')
        if book.attrs['href'] is not None:
            urlhref = book.attrs['href']
            href = urljoin(url,urlhref)
            # href = 'http://www.moe.gov.cn' + urlhref[1:]
            # href = href.replace('book', 'list')  # 需要把url中的book替换为list，直接进入章节页面
            bookName = book.text
            if bookName not in bookUrls:
                bookUrls[bookName] = href
                # print("{}:{}".format(bookName,href))

                print(bookUrls[bookName], '===========',  bookName)
    # for bookName in bookUrls.keys():
    #     getASection(bookUrls[bookName], bookName)

def getHtml(url):
    bs_xml = BeautifulSoup(url)

    print(bs_xml.prettify())

    div = bs_xml.findAll('div', {'class': 'nav'})

    div[0].contents
# 替换表情符号
def filter_emoji(desstr,restr=''):
    #过滤表情
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


getBooks('https://tieba.baidu.com/p/7210039130')





# 'http://www.moe.gov.cn/s5987/202101/t20210114_509847.html'
# url = "http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/"
# uri = "./s5987/202101/t20210105_508744.html"
# print(urljoin(url,uri))
# 'http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/s5987/202101/t20210105_508744.html'