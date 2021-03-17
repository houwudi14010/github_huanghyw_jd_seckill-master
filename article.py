from urllib.parse import urljoin, urlparse
import re

import furl as furl
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
database='article'
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
    response.encode = 'utf-8'
    content = response.text.encode(response.encoding).decode(response.apparent_encoding)
    soup = BeautifulSoup(content, 'lxml')
    #取出a标签 href属性 符合该正则关系式的 a标签
    urls = soup.find_all("a",attrs={'href':re.compile("http://www.douguo.com/article/detail/\d{1,10}")})
    for i in urls:
        cursor = conn.cursor()
        try:
            #取出所有的a标签里的href属性
            url = urljoin(response.url, i["href"])
            #排重所需要的url参数
            data = (url)
            query = 'select * from yq_article where article_onlyl_url = "%s"' % (str(data))
        except Exception as err:
            print("sql语句执行错误", err)
            conn.rollback()
        try:
            cursor.execute(query)
            #查询返回的参数
            result = cursor.fetchall()
            conn.commit()


            #如果存在 跳过此次循环 如果没有继续执行
            if result :
                continue

            else:

                # 取出域名
                res = urlparse(url)
                domain = res.netloc
                # 请求地址 获取网页源代码
                rsp = requests.get(url, headers=headers)
                bs = BeautifulSoup(rsp.content, 'html.parser', from_encoding='utf-8')
                # 正则匹配h1标签标题
                title = re.compile('<h3>(.*?)</h3>').findall(str(bs))
                # 取出该标签下的内容
                aa = bs.select('div.art-info')
                # 正则匹配时间
                time = re.compile('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}').findall(str(aa))
                times = time[0]
                # 循环获取的参数 拼出时间格式
                # for g in times:
                # e, r, t, y, u,v = times
                # dates = e + "-" + r + "-" + t + " " + y + ":" + u + ":"+ v
                # 时间格式转换
                b = datetime.datetime.strptime(times, '%Y-%m-%d %H:%M:%S')
                # 正则匹配来源
                souce = re.compile('来自：(.*?)</a>').findall(str(aa))
                # 取出正文内容
                content_html = bs.select('div.par')
                content = content_html[0].text
                content_html = content_html[0].prettify()
                ac = escape_string(content_html)
                download_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                article_site = '豆果美食网'
                data = (title[0],article_site,ac,download_time,content,url, b, souce[0], domain, )
                query = "INSERT INTO yq_article(article_title,article_site,article_contenthtml,article_download_time,article_content,article_url,article_pub_time,article_souce,article_domain) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (data)

                try:
                    cursor.execute(query)
                    conn.commit()

                except Exception as err:
                    print("sql语句执行错误", err)
                    conn.rollback()




        except:
            import traceback
            print(traceback.format_exc())







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
    str_x = "http://www.sxbid.com.cn/f/list-62c2de4e86fb410a93236757a3796623.html?pageNo=1&pageSize=15&accordToLaw=http://www.sxbid.com.cn/f/list-62c2de4e86fb410a93236757a3796623.html?pageNo=2&pageSize=15&accordToLaw=http://www.sxbid.com.cn/f/list-62c2de4e86fb410a93236757a3796623.html?pageNo=3&pageSize=15&accordToLaw=http://www.sxbid.com.cn/f/list-62c2de4e86fb410a93236757a3796623.html?pageNo=4&pageSize=15&accordToLaw="

    i = 0
    #while i<= 10:
    url = 'https://www.douguo.com/article/0'
    getarticle(url)
    urls = ['http://society.people.com.cn/index{}.html#fy01'.format(str(i))for i in range(1, 1)]
    for i in urls:
        print(i)







