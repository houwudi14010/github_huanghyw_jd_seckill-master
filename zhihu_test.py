# import execjs
#
# fmd5 = 'c96ba0bbaf2c398327043d9d62f44102'
# with open('g_encrypt.js', 'r') as f:
#     ctx1 = execjs.compile(f.read(), cwd=r'D:\github_huanghyw_jd_seckill-master\node_modules')
# encrypt_str = ctx1.call('b', fmd5)
# print(fmd5)
# print(encrypt_str)
import requests
import execjs
import hashlib
import re

url = "/api/v4/search_v3?t=general&q=%E5%A0%80%E4%B8%8E%E5%AE%AB%E6%9D%91&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0"

referer = "https://www.zhihu.com/search?type=content&q=%E5%A0%80%E4%B8%8E%E5%AE%AB%E6%9D%91"

f = "+".join(["3_2.0", url, referer, '"AABcnFvxsRKPTrMLtxJshFeclnY0iW-zs9s=|1613959184"'])

fmd5 = hashlib.new('md5', f.encode()).hexdigest()

with open('g_encrypt.js', 'r') as f:
    ctx1 = execjs.compile(f.read(), cwd=r'D:\github_huanghyw_jd_seckill-master\node_modules')
encrypt_str = ctx1.call('b', fmd5)
print(encrypt_str)
headers = {
    "referer": referer,
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    "cookie": 'd_c0="AABcnFvxsRKPTrMLtxJshFeclnY0iW-zs9s=|1613959184";',
    "x-api-version": "3.0.91",
    "x-zse-83": "3_2.0",
    "x-zse-86": "1.0_%s" % encrypt_str,
}
r = requests.get("https://www.zhihu.com" + url, headers=headers)
content = r.content.decode("utf-8")
urls = re.compile('"question":{"id":"(.*?)",').findall(str(content))
for i in url:
    print(i)