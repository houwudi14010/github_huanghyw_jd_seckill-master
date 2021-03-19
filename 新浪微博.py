import datetime
import hashlib
import re
import threading
import time

import requests
from bs4 import BeautifulSoup
from pymongo import InsertOne, collection, MongoClient

headers = {
    'authority': 'weibo.com',
    'sec-ch-ua': '^\\^Google',
    'accept': 'application/json, text/plain, */*',
    'x-xsrf-token': 'azVGwJAZUslClEPHpZmI-d6J',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://weibo.com/u/2828741892',
    'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
    'cookie': 'SINAGLOBAL=528688026201.6336.1613962949023; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWymNhhY0SzjnBEUszxE-S45JpX5KMhUgL.FoqcSK-NeoepShM2dJLoIfQLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1K2L1h5t; WBPSESS=rqSHduCmTE6mwR3AmolJkl1XkzTcvYH5iTl5vDV377sP2apMFgmeBM1RPARFGzDFwPQtkf_B9CtNPyzN3W0X0op8RUaIXVX5-qP3mBVzFCw93kKXKgefWjURtuolWbsL; ULV=1615965942520:4:2:1:9997432940735.62.1615965942341:1615532004936; ALF=1647566333; SSOLoginState=1616030333; SCF=ApM_kj7Dez93SnOvW5JWvXPR1nRXpfshE-RxvP3v0UrR-taOxIB6pkIwTnbSX9ub-faEyv3SIYiCFP-twlftxB0.; SUB=_2A25NVtotDeRhGeBI7lcW8i3NzzuIHXVuIkzlrDV8PUNbmtAKLROikW9NRpWnaBFV-ULlFmeRohznybJtmxpIB85m; XSRF-TOKEN=azVGwJAZUslClEPHpZmI-d6J',
}
paramss = (
    ('id', 'K48eEa5Vk'),
)

client = MongoClient('localhost', 27017)
print(client)  # 成功则说明连接成功
# 用户验证 连接mydb数据库,账号密码认证
db = client.article  # 连接对应的数据库名称，系统默认数据库admin

#db.authenticate('root', '你的密码password')

# 连接所用集合，也就是我们通常所说的表
collection = db.article_list_nimowen
def md5(str):
  m = hashlib.md5()
  m.update(str.encode("utf8"))
  return m.hexdigest()


def onlys (wy):
    wy = md5(wy)
    return wy
def insertdb (data):
    try:
        collection.bulk_write(data)
        print('添加完成')
    except:
        print('重复添加')
def trans_format(time_string, from_format, to_format='%Y.%m.%d %H:%M:%S'):
    """
    @note 时间格式转化
    :param time_string:
    :param from_format:
    :param to_format:
    :return:
    """
    time_struct = time.strptime(time_string,from_format)
    times = time.strftime(to_format, time_struct)
    return times
def article(url,contentURL,articleurl):
    try:
        ss = requests.Session()
        push_state = 0
        #site = "公主殿下的树洞"
        site_id = 521
        contentrsp = ss.get(contentURL,headers = headers)
        contentbs = BeautifulSoup(contentrsp.content, 'html.parser', from_encoding='utf-8')
        rsp = ss.get(url)
        bs = BeautifulSoup(rsp.content, 'html.parser', from_encoding='utf-8')
        site = re.compile('"screen_name":"(.*?)",').findall(str(bs))
        print(url)

        site = site[0]
        content = re.compile('"longTextContent":"(.*?)"}').findall(str(contentbs))
        only = re.compile('"mblogid":"(.*?)"').findall(str(bs))
        value = only[0]
        time = re.compile('"created_at":"(.*?)"').findall(str(bs))
        time = time[0]
        format_time = trans_format(time, '%a %b %d  %H:%M:%S +0800 %Y', '%Y-%m-%d %H:%M:%S')
        downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        wys = value+format_time
        wyss = onlys(wys)
        if content == []:
            title = re.compile('"text_raw":"(.*?)"').findall(str(bs))
            title = title[0]
            content = re.compile('"text":"(.*?)",').findall(str(bs))
            content = content[0]
            data = []
            data.append(InsertOne(
                {"url": url, "title": title, "aid": value, "content": content, "site": site, "pub_time": format_time,
                 "only_id": wyss, "push_state": push_state, "site_id": site_id,"download_Time":downloadTime}))
            insertdb(data)
            # imgurl = re.compile('"pic_ids":(.*?),"').findall(str(bs))
            # for i in imgurl:
            #     imgurl = i
            #     imgurl = "https://wx1.sinaimg.cn/orj360/"+imgurl+".jpg"
        else:
            content = content[0]
            title = content
            data = []
            data.append(InsertOne({"url": url, "title": title,"aid":value,"content":content,"site":site,"pub_time":format_time,"only_id":wyss,"push_state":push_state,"site_id":site_id,"download_Time":downloadTime}))
            insertdb(data)
    except Exception as err:
        print(err)
        pass
    # 关闭连接
    client.close()














def my_job():
    params = (
        ('uid', ''),
        ('page', '1'),
        ('feature', '0')
    )
    lisy = [1876879003,6586580900,1853850492,6512991534,2282795285,1843070674,2686579097,1916501605,2865341160,5703712834]
    for i in lisy:
        params = dict(params)
        params["uid"] = i
        print(params)
        response = requests.get('https://weibo.com/ajax/statuses/mymblog', headers=headers, params=params)

        #NB. Original query string below. It seems impossible to parse and
        #reproduce query strings 100% accurately so the one below is given
        #in case the reproduced version is not "correct".
        # response = requests.get('https://weibo.com/ajax/statuses/mymblog?uid=3266943013&page=1&feature=0', headers=headers)


        #NB. Original query string below. It seems impossible to parse and
        #reproduce query strings 100% accurately so the one below is given
        #in case the reproduced version is not "correct".
        # response = requests.get('https://weibo.com/ajax/statuses/mymblog?uid=3266943013&page=1&feature=0', headers=headers)


        #NB. Original query string below. It seems impossible to parse and
        #reproduce query strings 100% accurately so the one below is given
        #in case the reproduced version is not "correct".
        # response = requests.get('https://weibo.com/ajax/statuses/mymblog?uid=2656274875&page=3&feature=0', headers=headers)
        content = response.content.decode("utf-8")
        url = re.compile('mblogid":"(.*?)"').findall(str(content))
        for i in params:
            uid = i[1]
            break

        print(uid)
        for urls in url:
            ur = "https://weibo.com/ajax/statuses/show?id="+urls
            contentURL = "https://weibo.com/ajax/statuses/longtext?id="+urls
            articleurl = "https://weibo.com/"+uid+"/"+urls

            article(ur,contentURL,articleurl)
        #     #print(ur)
        # s = requests.Session()
        # response = s.get('http://www.xinhuanet.com/', headers=headers,params=params,  verify=False)

def func():
  # 每2s执行一次
  my_job()
  threading.Timer(30, func).start()


if __name__ == "__main__":
  a = {'x': 1}
  func()
