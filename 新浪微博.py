import datetime
import hashlib
import re
import threading
import time

import requests
from bs4 import BeautifulSoup
from pymongo import InsertOne, collection, MongoClient
ss = requests.Session()
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
}
old_cookies={
    'cookie':'SCF=ApM_kj7Dez93SnOvW5JWvXPR1nRXpfshE-RxvP3v0UrRMF3u5krfFkF8jrUTUujT29kCWTXyWRRPnnRBenInlzI.; SUB=_2A25NWHFpDeRhGeBI7lcW8i3NzzuIHXVuLOWhrDV8PUNbmtAfLW_9kW9NRpWnaAgtZpFn-06XxSCHJd_xUvTwHEz0;'
}


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
    downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        collection.bulk_write(data)
        collection.update_one(data, {'$set': data}, upsert=True)

        print('添加完成'+downloadTime)
    except:
        print('重复添加'+downloadTime)
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
def article(url,contentURL,articleurl,proxy):
    try:
        push_state = 0
        site_id = 521
        contentrsp = ss.get(contentURL,headers = headers,cookies = old_cookies,proxies=proxy)
        contentbs = BeautifulSoup(contentrsp.content, 'html.parser', from_encoding='utf-8')
        rsp = ss.get(url,proxies=proxy)
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
        downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(downloadTime)
        import traceback
        traceback.print_exc()
        pass
    # 关闭连接
    client.close()

def my_job():
    paramsss = (
        ('type', 'uid'),
        ('value', ''),
        ('containerid', '')
    )
    lisy = [2828741892,1876879003,2882591901,1853850492,6512991534,2282795285,1843070674,2686579097,1916501605,2865341160,5703712834]
    for i in lisy:
        try:
            agentUrl = "http://47.96.91.228:82/get/"
            res = requests.get(agentUrl)

            agenContent = res.content.decode("utf-8")
            dataip = re.compile('"proxy": "(.*?)",').findall(str(agenContent))
            ip = dataip[0]
            proxy = {
                'https://':ip,
            }

            requests.proxies = proxy
            paramsss = dict(paramsss)
            paramsss["value"] = i
            paramsss["containerid"] = '107603' + str(paramsss["value"])
            print(paramsss)
            #response = requests.get('https://weibo.com/ajax/statuses/mymblog', headers=headers, params=params,cookies=old_cookies)
            response = requests.get('https://m.weibo.cn/api/container/getIndex', params=paramsss)

            content = response.content.decode("utf-8")
            url = re.compile('mblogid=(.*?)&').findall(str(content))

            for urls in url:
                ur = "https://weibo.com/ajax/statuses/show?id="+urls
                contentURL = "https://weibo.com/ajax/statuses/longtext?id="+urls
                articleurl = "https://weibo.com/"+str(i)+"/"+urls
                article(ur, contentURL, articleurl, proxy)
        except Exception as err:
            import traceback
            traceback.print_exc()
            pass

        #     #print(ur)
        # s = requests.Session()
        # response = s.get('http://www.xinhuanet.com/', headers=headers,params=params,  verify=False)

def func():

    # 每2s执行一次
    my_job()
    threading.Timer(2, func).start()


if __name__ == "__main__":
  a = {'x': 1}
  func()
