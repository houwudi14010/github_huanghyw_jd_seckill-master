import hashlib
import re
import threading

import requests
import datetime
import time
from pymongo import InsertOne, collection, MongoClient


ss = requests.Session()
client = MongoClient('localhost', 27017)
print(client)  # 成功则说明连接成功
# 用户验证 连接mydb数据库,账号密码认证
db = client.article  # 连接对应的数据库名称，系统默认数据库admin

# db.authenticate('root', '你的密码password')

# 连接所用集合，也就是我们通常所说的表
collection = db.article_list_jiefang
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
        print('添加完成'+downloadTime)

    except Exception as err:
        import traceback
        traceback.print_exc()
        pass

def article(url,site,site_id,pid,push_state,downloadTime):
    try:
        rq = ss.get(url)
        content = rq.content.decode("utf-8")
        imgurl = re.compile('"url\\\\":\\\\"(.*?)\\\\"').findall(str(content))
        imgContent = ""
        for im in imgurl:
            if imgurl :
                imgContent += "<img src="+im+"><br>"
        #标题
        titleText = re.compile('"title":"(.*?)"').findall(str(content))
        titleText = titleText[0]
        #发布时间 时间戳 需要转换
        releaseTime = re.compile('"addtime":(.*?),"').findall(str(content))
        releaseTime = releaseTime[0]
        timeStamp = float(int(releaseTime) / 1000)
        timeArray = time.localtime(timeStamp)
        releaseTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        #唯一索引字段
        wys = pid + releaseTime
        wyss = onlys(wys)
        #正文内容
        contentText = re.compile('"content":"(.*?)",').findall(str(content))
        contentText = imgContent+contentText[0]
        #新增到数据库
        data = []
        data.append(InsertOne(
            {"url": url, "title": titleText, "aid": pid, "content": contentText, "site": site, "pub_time": releaseTime,
             "only_id": wyss, "push_state": push_state, "site_id": site_id, "download_Time": downloadTime}))
        insertdb(data)

    except Exception as err:
        import traceback
        traceback.print_exc()
        pass





def my_job():

    try:
        NowTime = time.localtime() #获取当前时间
        times = time.strftime("%Y-%m-%d", NowTime)
        response = ss.get('https://www.jfdaily.com/staticsg/data/journal/'+times+'/navi.json')

        #NB. Original query string below. It seems impossible to parse and
        #reproduce query strings 100% accurately so the one below is given
        #in case the reproduced version is not "correct".
        # response = requests.get('https://www.jfdaily.com/staticsg/data/journal/2021-04-02/navi.json?ver=1617330627219', headers=headers, cookies=cookies)
        content = response.content.decode("utf-8")
        title = re.compile('"articleid":(.*?),"[\s\S]*?."id":(.*?),"jdate":"(.*?)",').findall(str(content))
        site = "解放日报"
        site_id = 1043419
        push_state = 0
        downloadTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in title:
            articleid,pid,pushtime = i[0],i[1],i[2]
            if int(articleid[0:2]) >16:
                articleid = "0"+articleid[0]
            elif int(articleid) <= 16:
                articleid = "0"+articleid[0]
            articleid = articleid[0:2]
            url = "https://www.jfdaily.com/staticsg/data/journal/"+pushtime+"/"+articleid+"/article/"+pid+".json"
            article(url,site,site_id,pid,push_state,downloadTime)
    except Exception as err:
        import traceback
        traceback.print_exc()
        pass

def func():
    # 每2s执行一次
    my_job()
    threading.Timer(2, func).start()


if __name__ == "__main__":
  a = {'x': 1}
  func()
