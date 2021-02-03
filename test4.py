from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup



import tld as tld
import mysql.connector
import pymysql
import time
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from pymysql.converters import escape_string
conn=mysql.connector.connect(
user='root',
password='123456',
host='127.0.0.1',
port='3306',
database='test'
)

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
def getASection(url,title):
        cursor = conn.cursor()
        try:

            # f = open(bookName, "a", encoding='utf-8')  # 利用追加的方式打开文件，这样后面章节的内容不会覆盖前面章节
            rsp = requests.get(url, headers=headers)
            rsp.encoding = 'utf-8'
            n = 0
            bs = BeautifulSoup(rsp.text, 'html.parser')
            body = bs.select('div.d_post_content.j_d_post_content ')
            n = 0
            for i in body:
                bodys = body[n]
                content = bodys.text
                #bodys = "🙉🙉dsadsadasdas"
                bodyss = escape_string(filter_emoji(str(bodys), ''));
                contents = escape_string(filter_emoji(str(content), ''));
                n = n+1
                title = title
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                site = '中国政府网'
                data = (title, site,str(bodyss),times,contents)
                query = "INSERT INTO yq_article(article_title,article_site,article_contenthtml,article_download_time,article_content) VALUES ('%s','%s','%s','%s','%s')" % (data)
                try:
                    cursor.execute(query)
                    conn.commit()

                except Exception as err:
                    print("sql语句执行错误", err,query)
                    conn.rollback()
            cursor.close()
                # f.writelines(content)
                # f.close()
        except IndexError as e:
            print("======", e)


        finally:
            print('finally...')
def getarticle(url):
    response = requests.get(url, headers=headers)
    contents = response.text.replace("<!--",'').replace("-->",'')
    soup = BeautifulSoup(contents, 'lxml')
    urls = soup.find_all("a",attrs={'href':re.compile("^/p/\d+")})
    # urls = soup.find_all("a",attrs={'href':True})
    for i in urls:
        url = urljoin(response.url, i["href"])
        title = urljoin(response.url, i["title"])[24:]
        print(url,str(title))
        getASection(url,title)


# 替换表情符号
def filter_emoji(desstr,restr=''):
    #过滤表情
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    aa = co.sub(restr, desstr)
    return aa



def chachong(a):
    cursor = conn.cursor()
    query = 'select distinct article_title from yq_article'
    cursor.execute(query)
    aa = cursor.fetchall()

    print()
    for i in aa:
        print(i,'111',str(aa))
        if a in str(aa):
            print('1')
        else:
            print('2')

#getarticle('https://tieba.baidu.com/f?ie=utf-8&kw=%E6%A8%AA%E5%8E%BF&fr=search')

chachong("【关于横县鱼生】 发誓要做科普")