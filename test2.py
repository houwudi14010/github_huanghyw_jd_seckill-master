import threading
import urllib.parse as urlparse

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from threading import Timer

from bs4 import BeautifulSoup
from numpy.core.tests.test_einsum import chars
from selenium.webdriver.chrome import webdriver
from self import self

import schedule
import hashlib
import re
import time,datetime
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
    'JSESSIONID': '85D47A466A4491FF9B842F832DBD5023',
}

headers = {

}

data = {
  'javax.faces.ViewState': 'j_id3:j_id9',
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

def articleURL(url,site):
  # 取出中文

  # 取出域名
  parsed = urlparse.urlparse(url)
  querys = urlparse.parse_qs(parsed.query)
  querys = {k: v[0] for k, v in querys.items()}
  aa = 0
  for value in querys.values():
    aa = aa+1
    if aa>1:
      break


  # 请求地址 获取网页源代码
  rsp = requests.get(url, headers=headers)
  bs = BeautifulSoup(rsp.content, 'html.parser', from_encoding='utf-8')
  content = str(bs)
  content_html = re.compile('<tr class="\w*" id="form:reFreshData_row_\d">[\s\S]*?.</tr>').findall(content)
  # 取出标题
  title = bs.select('title')
  title = title[0]
  title = title.text
  ss = 0
  push_state = 0
  siteid = 1038898
  for i in content_html:
    #取出发表时间
    time = re.compile('发表于：<label>\s*(.*?)\</label>').findall(str(content_html))
    time = time[ss]
    time = time.replace("\\n", "")
    # = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    #取出正文
    content = re.compile('<span style="word-break:break-all;">(.*?)</span>').findall(str(content_html))
    content = content[ss]
    md = re.compile('openAuthor\((.*?)\)').findall(str(content_html))
    md = md[ss]
    wy = str(md)+str(time)
    wy = md5(wy)
    ss = ss+1
    data = []
    data.append(InsertOne({"url": url, "title": title,"aid":value,"content":content,"site":site,"pub_time":time,"only_id":wy,"push_state":push_state,"site_id":siteid}))
    try:

      collection.bulk_write(data)
    except:
      import traceback
      continue
    # 关闭连接
    client.close()

def my_job(job_id="xxx"):
  print("===========")
  try:

    ac = 1
    bc = 0
    s = requests.Session()
    data['form:refreshData_first'] = bc
    data['form:refreshData_page'] = ac

    response = s.post('http://fuwu.siyang.gov.cn:9000/siyang/network.seam', data = data,headers=headers, cookies=cookies, verify=False,timeout = 50)
    ss = response.content.decode("utf-8")
    url = re.compile('href="(.*?)"').findall(str(ss))
    site = '泗水阳春论坛'
    bc = bc + 20
    ac = ac + 1

    for i in url:
      article_url = 'http://fuwu.siyang.gov.cn:9000/' + i
      articleURL(article_url,site)



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
  threading.Timer(2, func).start()


if __name__ == "__main__":
  a = {'x': 1}
  func()

