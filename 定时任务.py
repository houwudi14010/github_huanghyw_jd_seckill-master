# -*- coding:utf-8 -*-
import time
import datetime

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

def my_job(text="默认值"):



    print("================")


# sched.add_job(my_job, 'interval', seconds=3, args=['3秒定时'])
# # 2018-3-17 00:00:00 执行一次，args传递一个text参数
# sched.add_job(my_job, 'date', run_date=datetime.date(2019, 10, 17), args=['根据年月日定时执行'])
# # 2018-3-17 13:46:00 执行一次，args传递一个text参数
# sched.add_job(my_job, 'date', run_date=datetime.datetime(2019, 10, 17, 14, 10, 0), args=['根据年月日时分秒定时执行'])
# sched.start()
"""
interval 间隔调度，参数如下：
    weeks (int) – 间隔几周
    days (int) – 间隔几天
    hours (int) – 间隔几小时
    minutes (int) – 间隔几分钟
    seconds (int) – 间隔多少秒
    start_date (datetime|str) – 开始日期
    end_date (datetime|str) – 结束日期
    timezone (datetime.tzinfo|str) – 时区
"""
"""
cron参数如下：
    year (int|str) – 年，4位数字
    month (int|str) – 月 (范围1-12)
    day (int|str) – 日 (范围1-31)
    week (int|str) – 周 (范围1-53)
    day_of_week (int|str) – 周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun)
    hour (int|str) – 时 (范围0-23)
    minute (int|str) – 分 (范围0-59)
    second (int|str) – 秒 (范围0-59)
    start_date (datetime|str) – 最早开始日期(包含)
    end_date (datetime|str) – 最晚结束时间(包含)
    timezone (datetime.tzinfo|str) – 指定时区
"""
sched = BlockingScheduler()

def xunhuan():
 while True:my_job()

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
sched.add_job(my_job, 'cron', second='*/5', args=['5秒定时'])

sched.start()