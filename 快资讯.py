import re
import threading
import requests
import time
import hashlib
from bs4 import BeautifulSoup
from pymongo import MongoClient, InsertOne
client = MongoClient('localhost', 27017)
print(client)  # 成功则说明连接成功
# 用户验证 连接mydb数据库,账号密码认证
db = client.article  # 连接对应的数据库名称，系统默认数据库admin

#db.authenticate('root', '你的密码password')
ss = requests.Session()
# 连接所用集合，也就是我们通常所说的表
collection = db.article_list_kuaizixun
headers = {
    'authority': 'papi.look.360.cn',
    'sec-ch-ua': '^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-dest': 'script',
    'referer': 'https://www.360kuai.com/',
    'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
    'cookie': 'tt_dsid=fdasof09vni234NGVjMGNhNWQwOTk0ZjQ5NGEzZmRlMzA2YTU5MmI3YTI=; xxl_city_code=local_BeiJing',
}

params = (
    ('scheme', 'https'),
    ('cur_rawurl', 'http^%^3A^%^2F^%^2Fzm.news.so.com^%^2Ff23f0a792bc672ee333939966b5ee782'),
    ('cur_title', '^%^E5^%^A5^%^B9^%^E4^%^B8^%^80^%^E6^%^AF^%^95^%^E4^%^B8^%^9A^%^E5^%^B0^%^B1^%^E4^%^B8^%^BB^%^E6^%^8C^%^81^%^E5^%^A4^%^AE^%^E8^%^A7^%^86^%^E6^%^98^%^A5^%^E6^%^99^%^9A^%^EF^%^BC^%^8C^%^E7^%^BE^%^8E^%^E5^%^88^%^B0^%^E4^%^B8^%^A4^%^E4^%^BA^%^BA^%^E4^%^B8^%^BA^%^E5^%^A5^%^B9^%^E5^%^87^%^80^%^E8^%^BA^%^AB^%^E5^%^87^%^BA^%^E6^%^88^%^B7^%^EF^%^BC^%^8C^%^E4^%^BB^%^8A43^%^E5^%^B2^%^81^%^E4^%^BC^%^BC^%^E5^%^B0^%^91^%^E5^%^A5^%^B3'),
    ('uid', '4ec0ca5d0994f494a3fde306a592b7a2'),
    ('u', '4ec0ca5d0994f494a3fde306a592b7a2'),
    ('tj_cmode', 'pclook'),
    ('tj_url', ''),
    ('v', '1'),
    ('sv', '8'),
    ('n', '10'),
    ('ufrom', '1'),
    ('outPutReplacePic', ''),
    ('action', '2'),
    ('f', 'jsonp'),
    ('market', 'pc_def'),
    ('stype', 'portal'),
    ('callfrom', 'detail'),
    ('newest_showtime', ''),
    ('oldest_showtime', ''),
    ('sign', 'look'),
    ('version', '2.0'),
    ('sqid', ''),
    ('device', '2'),
    ('net', '4'),
    ('where', 'detail'),
    ('refer_scene', ''),
    ('djsource', ''),
    ('gnid', '997272353cd8ac4f0'),
    ('tmprtp', ''),
    ('hsid', '0d00714d5c9d257c05493b3617de6767'),
    ('_t', '1615889269377'),
    ('c', 'youlike'),
    ('scene', '2'),
    ('min_text_n', '3'),
    ('reqtimes', '17'),
)
def md5(str):
  m = hashlib.md5()
  m.update(str.encode("utf8"))
  return m.hexdigest()


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://papi.look.360.cn/mlist?scheme=https&callback=jQuery19107570587610169701_1615887672810&cur_rawurl=http^%^3A^%^2F^%^2Fzm.news.so.com^%^2Ff23f0a792bc672ee333939966b5ee782&cur_title=^%^E5^%^A5^%^B9^%^E4^%^B8^%^80^%^E6^%^AF^%^95^%^E4^%^B8^%^9A^%^E5^%^B0^%^B1^%^E4^%^B8^%^BB^%^E6^%^8C^%^81^%^E5^%^A4^%^AE^%^E8^%^A7^%^86^%^E6^%^98^%^A5^%^E6^%^99^%^9A^%^EF^%^BC^%^8C^%^E7^%^BE^%^8E^%^E5^%^88^%^B0^%^E4^%^B8^%^A4^%^E4^%^BA^%^BA^%^E4^%^B8^%^BA^%^E5^%^A5^%^B9^%^E5^%^87^%^80^%^E8^%^BA^%^AB^%^E5^%^87^%^BA^%^E6^%^88^%^B7^%^EF^%^BC^%^8C^%^E4^%^BB^%^8A43^%^E5^%^B2^%^81^%^E4^%^BC^%^BC^%^E5^%^B0^%^91^%^E5^%^A5^%^B3&uid=4ec0ca5d0994f494a3fde306a592b7a2&u=4ec0ca5d0994f494a3fde306a592b7a2&tj_cmode=pclook&tj_url=&v=1&sv=8&n=10&ufrom=1&outPutReplacePic=&action=2&f=jsonp&market=pc_def&stype=portal&callfrom=detail&newest_showtime=&oldest_showtime=&sign=look&version=2.0&sqid=&device=2&net=4&where=detail&refer_scene=&djsource=&gnid=997272353cd8ac4f0&tmprtp=&hsid=0d00714d5c9d257c05493b3617de6767&_t=1615889269377&c=youlike&scene=2&min_text_n=3&reqtimes=17&_=1615887672867', headers=headers)


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://papi.look.360.cn/tag_list?callback=jQuery191030178249277321445_1615888807241&scene=nh2_1&refer_scene=nh2_1&u=4ec0ca5d0994f494a3fde306a592b7a2&sign=look&sqid=&n=20&stype=portal&tj_cmode=pclook&tj_url=&djsource=&version=2.0&device=2&action=1&ufrom=1&sv=4&net=4&market=pc_def&where=new_second&v=1&f=jsonp&scheme=https&tmprtp=&c=y1^%^3Adomestic&_=1615888807242', headers=headers)


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://m.look.360.cn/transcoding?callback=jQuery19108678869398415983_1615887565219&url=99ab0188bed7661e2&uid=4ec0ca5d0994f494a3fde306a592b7a2&sign=look&outPutReplacePic=&direct=data&page=&f=jsonp&scheme=https&_=1615887565236', headers=headers, cookies=cookies)

def my_job():
    try:
        response = requests.get('https://papi.look.360.cn/mlist', headers=headers, params=params)
        response = response.content.decode("utf-8")
        url = re.compile('"gnid":"(.*?)",').findall(str(response))
        site = "快资讯-网站"
        siteid = 1039033
        push_state = 0
        for i in url:

                print()
                url = "https://m.look.360.cn/transcoding?callback=jQuery19108678869398415983_1615887565214&direct=data&url=" + i
                urls = "https://www.360kuai.com/" + i
                contentrsp = ss.get(url)
                contentbs = BeautifulSoup(contentrsp.content, 'html.parser', from_encoding='utf-8')
                contentbs = str(contentbs)
                content = re.compile('"content\\\\":\\\\"(.*?).",').findall(contentbs)
                content = content[0]
                content = content.replace('\\u003c','<')
                content = content.replace('\\u003e', '>')
                txt = re.sub("<[^>]*?>","",content)
                title = re.compile('"title\\\\":\\\\"(.*?).",').findall(contentbs)
                for t in title:
                    title = t
                print(title)
                times = re.compile('"pub_time\\\\":(.*?).,').findall(contentbs)
                times = times[0]
                times = times[0:10]
                times = int(times)
                timeArray = time.localtime(times)
                end_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                print(end_time)
                wy = i + end_time
                value = md5(wy)
                data = []
                data.append(InsertOne(
                    {"url": urls, "title": title, "aid": value, "content": txt, "site": site, "pub_time": end_time,
                     "only_id": value, "push_state": push_state, "site_id": siteid}))
                try:
                    collection.bulk_write(data)
                except:
                    import traceback
                # 关闭连接
                client.close()
    except:
        pass
def func():
  # 每2s执行一次
  my_job()
  threading.Timer(2, func).start()


if __name__ == "__main__":
  a = {'x': 1}
  func()