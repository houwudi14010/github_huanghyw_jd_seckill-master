import threading

import requests

from bs4 import BeautifulSoup

import hashlib
import re
from pymongo import MongoClient, InsertOne

import sched

client = MongoClient('localhost', 27017)
print(client)  # 成功则说明连接成功
# 用户验证 连接mydb数据库,账号密码认证
db = client.article  # 连接对应的数据库名称，系统默认数据库admin

#db.authenticate('root', '你的密码password')

# 连接所用集合，也就是我们通常所说的表
collection = db.article_list
cookies = {
    'uid': '85630c743c014b538e14d9b9a7831516',
    'wdcid': '5514aede23918042',
    'pc': '8447c974605386461312a244c9b889fc.1588943861.1588943861.1',
    'tma': '182794287.65540369.1591235049019.1591235049019.1591235049019.1',
    'fingerprint': '7e6deec267d01c2e6afa246b87b6d9c3',
    'bfd_g': '87205254007bf95200005f7b054efcc45e44ee82',
    'bfdid': '87205254007bf95200005f7b054efcc45e44ee82',
}

headers = {

}

data = {
  'javax.faces.ViewState': 'j_id9:j_id15',
  'primefacesPartialRequest': 'true',
  'form:refreshData_paging': 'true',
  'form:refreshData_first': '0',
  'form:refreshData_rows': '20',
  'form:refreshData_page': '1',
  'primefacesPartialSource': 'form:refreshData',
  'primefacesPartialProcess': 'form:refreshData'
}


def md5(str):
  m = hashlib.md5()
  m.update(str.encode("utf8"))
  return m.hexdigest()


def md5GBK(str1):
  m = hashlib.md5(str1.encode(encoding='gb2312'))
  return m.hexdigest()
def ccc ():
    print("111")
def articleURL(value,url,site):
    # 取出中文


    value = value[0]
    ss = 0
    # 请求地址 获取网页源代码
    rsp = requests.get(url, headers=headers)
    bs = BeautifulSoup(rsp.content, 'html.parser', from_encoding='utf-8')
    title = bs.select("span.title")
    title = title[0]
    title = title.text
    content = str(bs)
    content_html = re.compile('<div id="detail">[\s\S]*?.</div>').findall(content)
    content_html = content_html[ss]
    dr = re.compile(r'<[^>]+>', re.S)
    content_html = dr.sub('', content_html)
    content_html = content_html.replace("\n", "")

    push_state = 0
    siteid = 1038904
    #取出发表时间
    time = re.compile('<span class="year"><em> (.*?)</em></span><span class="day"><em> (.*?)</em>/<em> (.*?)</em></span><span class="time"> (.*?):(.*?):(.*?)</span>').findall(content)
    for o in time:
        a,b,c,d,e,f,= o[0],o[1],o[2],o[3],o[4],o[5],
        print(a,b,c,d,e,f)
        time = a+"-"+b+"-"+c+" "+d+":"+e+":"+f
        #取出正文
        wy = time+str(value)
        wy = md5(wy)
        ss = ss+1
        data = []
        data.append(InsertOne({"url": url, "title": title,"aid":value,"content":content_html,"site":site,"pub_time":time,"only_id":wy,"push_state":push_state,"site_id":siteid}))
        try:
            collection.bulk_write(data)
        except:
            import traceback
        # 关闭连接
        client.close()

def my_job(job_id="xxx"):
  print("===========")
  try:

    s = requests.Session()
    response = requests.get('http://www.xinhuanet.com/', headers=headers, cookies=cookies, verify=False)
#    response = s.post('http://www.xinhuanet.com/', headers=headers, cookies=cookies, verify=False)
    ss = response.content.decode("utf-8")
    url = re.compile('<h1><a href="(.*?)"').findall(str(ss))
    bs = BeautifulSoup(response.text, 'html.parser')
    ac = bs.select("div.box.headline")
    url = re.compile('<a href="(.*?)" target="_blank">').findall(str(ac))
    site = '习近平的两会时间'
    for i in url:
      article_url = i
      value = re.compile('c_(.*?).htm').findall(article_url)
      if value == []:
          continue
      else:
        try:

            articleURL(value,article_url,site)
        except:
            pass



  except Exception as err:
    print(err)



# sched = BlockingScheduler()





# my_job将会在6,7,8,11,12月的第3个周五的1,2,3点运行
#sched.add_job(my_job, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
# 截止到2018-12-30 00:00:00，每周一到周五早上五点半运行job_function
#sched.add_job(my_job, 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2018-12-31')

# 京东白酒秒杀
#sched.add_job(xunhuan, 'cron', year=2021, month=1, day=22, hour=9, minute=59, second=58)

# 表示任务在6,7,8,11,12月份的第三个星期五的00:00,01:00,02:00,03:00 执行该程序
#sched.add_job(my_job, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')

# 表示从星期一到星期五5:30（AM）直到2014-05-30 00:00:00
#sched.add_job(my_job, 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2014-05-30')

# 表示每5秒执行该程序一次，相当于interval 间隔调度中seconds = 5
# sched.add_job(my_job, 'cron', second='*/5', args=['5秒定时'])
#
# sched.start()

def timedTask():
  print("1111")






def func():
  # 每2s执行一次
  my_job()
  threading.Timer(30, func).start()


if __name__ == "__main__":
  a = {'x': 1}
  func()

