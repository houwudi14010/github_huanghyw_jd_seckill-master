# -*- coding:utf-8 -*-
import time
import datetime

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

def my_job(text="默认值"):
    url = 'https://marathon.jd.com/seckillnew/orderService/submitOrder.action?skuId=100012043978'
    headers = {'Host': 'marathon.jd.com', 'Connection': 'keep-alive', 'Content-Length': '725',
               'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'jdapp;android;9.3.4;10;3353139323231303139333039333-13D2464353338333633633265303;network/wifi;model/SM-G9730;addressid/541283091;aid/9754014e6890f575;oaid/;osVer/29;appBuild/86388;partner/ks003;eufv/1;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 10; SM-G9730 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded', 'Origin': 'https://marathon.jd.com',
               'X-Requested-With': 'com.jingdong.app.mall', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Dest': 'empty',
               'Referer': 'https://marathon.jd.com/seckillM/seckill.action?skuId=100012043978&num=1&rid=1611194414',
               'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6'}
    cookies = {'pt_pin': 'jd_751253e85915d', 'pwdt_id': 'jd_751253e85915d',
               'shshshfpb': 'ybSeqvh5%20JEtmwgm1%209R7ag%3D%3D',
               'shshshfpa': '53592c9d-3e75-8116-a159-61b1bed0b86a-1568271477', 'webp': '1',
               'visitkey': '30574749819088452', '__jdu': '1599294368019615186716', '__jdc': '121091540',
               'cartLastOpTime': '1604302529', 'cartNum': '66', 'retina': '1', 'cid': '8', 'sc_width': '412',
               '__wga': '1609381907267.1609381833515.1601654413091.1599873116287.3.3',
               'qd_uid': 'KJEKV7SM-DXGA00WO6SQVBB3252ZE', 'qd_fs': '1609523721523',
               '3AB9D23F7A4B3C9B': 'A6G4WECZFD4SUKCD5B5ZBZD7276J5F4FTQERPT7HJFZDTDG4AM7N36IUETYLVOIOZJQHH55VVOJH72VEA5QYDWFOYE',
               'plusCustomBuryPointToken': '1609899506149_4020',
               'unpl': 'ADC_9J7h8CFEjeiZuIWYHuZ%2BCrNhVG7dOdgujU70d%2BB3y4HOfinAIhI6K%2B%2FRLSroNFtc%2FpQXOk8%2FPrUymgzBzyoRCQv5VHAYIhT55Z1KgY5oO9GH2jIX7m4wgyYbMtGIPdrQe3onSXYOoM5Xcnsnkm8nSpvauoRUS%2BD7LOgcBb8O5oE%3D%7CV2_ZzNtbUtVRBMnDREEeBhYBGIDRl8RXkYWdwwWU3kRXlIwAxteclRCFnUUR1RnGF8UZgMZWUJcQBJFCEJkexhdBGUAEV1LVnMVdgpHV3IpVWtkBhJbQ19CF3JmRlV6dx5RN0BABHJUQyV0OE5SfxxdBWJXFVRKVhQRcwx2ZHIYbAduChdUQlFzzMq8ktXezvuzs761bUNnQiV0OBA6exhdBGYKEF1AUw4dcwxDVXscCAJuCxMKRlFHJXQ4Rg%3D%3D',
               'qd_ls': '1610509295215', 'qd_ts': '1610523565370', 'qd_sq': '5',
               'pt_key': 'app_openAAJgBnY3ADBAUxyW5Ww6hDB-69Rq9TjsKDFsepcUrEk02FieAq5423RmTRy5-Fzre3os8VgoFDg',
               'sid': 'e010a3e0085dc13bf52fd9bf686a1c7w', 'shshshfp': '2ddc1eee64a9c04f322daa3eeb791182',
               'BATQW722QTLYVCRD': '{"tk":"jdd01HXYPM42UYSBPF6RTC4VFWRBLTZLISOIWGZTLWQMLYOQCURLNXBCJPMSL5NJT4SC6XLIYZQIN32S65P4S6DSOQWHRX25EC55TNPV3JFQ01234567","t":1611062224647}',
               '__jda': '121091540.1599294368019615186716.1599294368.1611112837.1611193788.68',
               'mt_xid': 'V2_52007VwMWWlVbWl8dThBdBW8EElZdUVVcH04pWFcwChNUCV5OUkhIEUAANAYQTlRQB1MDQUsLBDAFQgFUDAEJL0oYXwV7AhJOXlhDWxdCHVsOZgYiUG1aYlkeTxFZAFcBFVFZ',
               '__jdv': '121091540%7Ckong%7Ct_1000170135%7Ctuiguang%7Cnotset%7C1611194163277', 'mobilev': 'touch',
               'pre_session': 'GOXa9NUHzRSCWAfne2Gm6uV7HppCdXlpS2tZ+drasWs', 'pre_seq': '4', 'wxa_level': '1',
               '__jdb': '121091540.5.1599294368019615186716|68.1611193788', 'mba_sid': '628.10',
               '__jd_ref_cls': 'RankingList_HotSaleMain3_Product',
               'mba_muid': '1599294368019615186716.628.1611194179650', 'seckillSku': '100012043978',
               'mid': 'imUkt8mpbevEc8F1puG5xQs1cuuiJsfaYi3Uetie4uI', 'seckillSid': ''}
    data = {'num': '2', 'addressId': '541283091', 'yuShou': 'true', 'isModifyAddress': 'false',
            'name': '%E7%8E%8B%E7%A7%8B%E6%B7%9E', 'provinceId': '1', 'provinceName': '%E5%8C%97%E4%BA%AC',
            'cityId': '2901', 'cityName': '%E6%98%8C%E5%B9%B3%E5%8C%BA', 'countyId': '55549',
            'countyName': '%E5%8C%97%E4%B8%83%E5%AE%B6%E9%95%87', 'townId': '0', 'townName': '',
            'addressDetail': '%E4%B8%9C%E4%B8%89%E6%97%97%E6%9D%91106%E5%8F%B7', 'mobile': '155%2A%2A%2A%2A1203',
            'mobileKey': 'c4df8ae67256b5f7aeb91d021a0d312f', 'email': '', 'invoiceTitle': '4', 'invoiceCompanyName': '',
            'invoiceContent': '1', 'invoiceTaxpayerNO': '', 'invoiceEmail': '',
            'invoicePhone': '155%252A%25%2A%2A%2A%2AA%252A1203',
            'invoicePhoneKey': '568d8e91c80f9b174b3179a637809846aeb91d021a0d312f', 'invoice': 'true', 'password': '',
            'codTimeType': '3', 'paymentType': '4', 'overseas': '0', 'phone': '', 'areaCode': '86',
            'token': 'aefc1550085915abd95f3abfde85b4cf'}

    html = requests.post(url, headers=headers, verify=False, cookies=cookies, data=data)
    print(len(html.text))
    print(html.text)

sched = BlockingScheduler()
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
sched.add_job(my_job, 'cron', second='*/1', args=['5秒定时'])

sched.start()