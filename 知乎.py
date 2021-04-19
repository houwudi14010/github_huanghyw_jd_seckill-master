import datetime
import re
import threading
import requests
from bs4 import BeautifulSoup
from pymongo import InsertOne, collection, MongoClient
import hashlib

site = "知乎"
push_state = 0
site_id = 521


client = MongoClient('localhost', 27017)
print(client)  # 成功则说明连接成功
# 用户验证 连接mydb数据库,账号密码认证
db = client.article  # 连接对应的数据库名称，系统默认数据库admin

#db.authenticate('root', '你的密码password')

# 连接所用集合，也就是我们通常所说的表
collection = db.article_list_zhihu
ss = requests.Session()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'x-zse-86': '2.0_aMFBk4r0HG2Xk028f7FqFUL8HBNYrTF8fHtygh90S8SX',
    'x-zse-83': '3_2.0',
    'cookie': 'd_c0="AABcnFvxsRKPTrMLtxJshFeclnY0iW-zs9s=|1613959184";'
}
headerss = {
    'authority': 'www.zhihu.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
}

params = (
    ('t', 'general'),
    ('q', '\u8FDB\u51FB\u7684\u5DE8\u4EBA'),
    ('correction', '1'),
    ('offset', '0'),
    ('limit', '20'),
    ('lc_idx', '0'),
    ('show_all_topics', '0'),
)
def md5(str):
  m = hashlib.md5()
  m.update(str.encode("utf8"))
  return m.hexdigest()
def onlys (wy):
    wy = md5(wy)
    return wy
def insertdb (data,downloadTime):
    try:
        collection.bulk_write(data)
        print('添加完成')
        print(downloadTime)
    except:
        print('重复添加')


def article(i):
    io = 0
    try:
        urlList = "https://www.zhihu.com/question/"+i
        responses = requests.get(urlList,headers=headerss)
        contents = responses.content.decode("utf-8")
        author = re.compile('authorName&quot;:(.*?),').findall(str(contents))
        title = re.compile('title":"(.*?)",').findall(str(contents))
        title = title[0]
        for b in author:
            bs = BeautifulSoup(responses.text, 'html.parser')
            content = bs.select("div.RichContent-inner")
            content = content[io].text
            time = re.compile('<span data-tooltip="发布于(.*?)"').findall(str(contents))
            time = datetime.datetime.strptime(time[io], ' %Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M:%S')
            downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            wys = i+time
            wyss = onlys(wys)
            data = []
            data.append(InsertOne(
                {"url": urlList, "title": title, "aid": time, "content": content, "site": site, "pub_time": time,
                 "only_id": wyss, "push_state": push_state, "site_id": site_id, "download_Time": downloadTime}))
            insertdb(data,downloadTime)
            io = io + 1
    except Exception as err:
        print(err)
        pass
def my_job():
    response = ss.get('https://www.zhihu.com/api/v4/search_v3', headers=headers, params=params)

    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://www.zhihu.com/api/v4/search_v3?t=general&q=%E7%94%B5%E6%A2%AF&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0', headers=headers)

    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://www.zhihu.com/api/v4/search_v3?t=general&q=^%^E7^%^94^%^B5^%^E6^%^A2^%^AF&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0', headers=headers)
    content = response.content.decode("utf-8")
    url = re.compile('"question":{"id":"(.*?)",').findall(str(content))
    for i in url:
        article(i)

def func():
    # 每2s执行一次
    my_job()
    threading.Timer(60, func).start()


if __name__ == "__main__":
    a = {'x': 1}
    func()