from urllib.parse import urljoin
import re
from bs4 import BeautifulSoup


import time,datetime
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
def getASection(aa,title):
        cursor = conn.cursor()
        try:
            # aa = 'https://tieba.baidu.com/p/7198585197'
            # f = open(bookName, "a", encoding='utf-8')  # 利用追加的方式打开文件，这样后面章节的内容不会覆盖前面章节
            rsp = requests.get(aa)
            rsp.encoding = 'utf-8'
            bs = BeautifulSoup(rsp.content, 'lxml', from_encoding='utf-8')
            body = bs.select('div.d_post_content_main ')
            bodyTime = bs.select('div.d_post_content_main.d_post_content_firstfloor')
            author = bs.select('a.p_author_name.j_user_card')
            fabutime = bs.select('span.tail-info')
            # print(fabutime)
            n = 0
            for i in body:
                authorss = author[n]
                authors = authorss.text
                bodys = body[n]
                content = bodys.text
                bodyss = escape_string(filter_emoji(str(bodys), ''));
                contents = escape_string(filter_emoji(str(content), ''));
                ax =re.compile("post_content_\d{1,20}").findall(str(bodys))
                contentsss = re.compile('<div class="d_post_content j_d_post_content" .*?>.*?</div>').findall(str(bodys))
                onlys = re.sub("\D", '', str(ax))
                only = aa + '?pid=' + onlys + '#' + onlys
                b = contentsss[0]
                s2 = re.sub(r'<.*?>', '', b)
                avc = re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}', str(bodys))
                n = n+1
                title = title
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                timesss = datetime.datetime.strptime(str(avc[0]), "%Y-%m-%d %H:%M")
                site = '王者荣耀cp吧'
                article_url = aa
                data = (title, site,str(b),times,s2,authors,article_url,only,timesss)
                query = "INSERT INTO yq_article(article_title,article_site,article_contenthtml,article_download_time,article_content,article_author,article_url,article_onlyl_url,article_pub_time) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (data)
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
    #取出a标签 href属性 符合该正则关系式的 a标签
    urls = soup.find_all("a",attrs={'href':re.compile("^/p/\d+")})

    for i in urls:
        url = urljoin(response.url, i["href"])
        title = urljoin(response.url, i["title"])[24:]
        print(url,str(title))
        rsp = requests.get(url, headers=headers)
        # rsp.encoding = 'utf-8'
        bs = BeautifulSoup(rsp.content,'html.parser',from_encoding='utf-8')
        aa = bs.select('li.l_pager.pager_theme_4.pb_list_pager')
        ac = re.compile('pn=\d{1,20}">尾')
        num = ac.findall(str(aa))
        a = 0
        if num:
            num = re.sub("\D", '', str(num))
            for c in range(int(num)):
                print(c)
                while a <= c:
                    a += 1
                    ur = url + '?pn=' + str(a)
                    print(ur+'请求的地址')
                    getASection(ur, title)
        else:
                getASection(url, title)

# 替换表情符号
def filter_emoji(desstr,restr=''):
    #过滤表情
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    aa = co.sub(restr, desstr)
    return aa



a = 0
#今天的日期
print(datetime.date.today())
if 0> 1:

    getarticle('https://app.peopleapp.com/WapApi/610/HomeApi/getContentList?category_id=1&refresh_time='+time.time()+'&show_num=10&page=1&securitykey=fc49714a2d13235bd10fa96e21c2a2be&interface_code=610')
else:
    # num = i * 50
    # urls = 'https://tieba.baidu.com/p/7210039130?pn='
    i = 0
    while i<= 10:
        url = "https://tieba.baidu.com/f?kw=%E7%8E%8B%E8%80%85%E8%8D%A3%E8%80%80cp&ie=utf-8&pn="
        num = i * 50
        print(url+str(num))
        getarticle(url+str(num))
        i = i + 1
    # a = 1
    # for i in range(2):
    #     a += 1
    #     print(urls+str(a))
    #     getASection(urls+str(a),'把你们这些处CP的都给记下来')


