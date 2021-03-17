import re

import requests

import requests
import urllib.parse
import requests
from bs4 import BeautifulSoup


#def articleURL(url,site):
# 取出中文
url = 'http://zhidao.baidu.com/question/2142772190297550748.html?fr=iks&word=%CD%A3%B5%E7&ie=gbk'
value = re.compile('question/(.*?).htm').findall(url)
value = value[0]
ss = 0
# 请求地址 获取网页源代码
rsp = requests.get(url,)
bs = BeautifulSoup(rsp.content, 'html.parser', from_encoding='utf-8')
content = str(bs)
content_html = re.compile('<div id="detail">[\s\S]*?.</div>').findall(content)
content_html = content_html[ss]
dr = re.compile(r'<[^>]+>', re.S)
content_html = dr.sub('', content_html)
content_html = content_html.replace("\n", "")
print(content_html)
# 取出标题
title = bs.select('span.title')
title = title[0]
title = title.text
title = title.replace("\r\n", "")
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













#
#
#
# cookies = {
#     'BIDUPSID': '208F3FFB79BE951B1776C8B8D97F8AA9',
#     'PSTM': '1613956978',
#     '__yjs_duid': '1_9187501c2c8129a6587c232008428dcf1613958606958',
#     'BDUSS': '0xY2FDaUhGTmdKdlJWTUw2QkNiM3JOS1kzbGYyc2JvMURPamdsSnpWSHVvVnBnRVFBQUFBJCQAAAAAAAAAAAEAAAAb6XQ072LgkwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO4UM2DuFDNgUi',
#     'BDUSS_BFESS': '0xY2FDaUhGTmdKdlJWTUw2QkNiM3JOS1kzbGYyc2JvMURPamdsSnpWSHVvVnBnRVFBQUFBJCQAAAAAAAAAAAEAAAAb6XQ072LgkwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO4UM2DuFDNgUi',
#     'BAIDUID': '610EBE2F82C4CC5572E7C40E2E769875:FG=1',
#     'BDSFRCVID': 'UIDOJexroG3Vd5oe8hCLb4DmEoizkVOTDYrEOwXPsp3LGJLVgVMXEG0PtEhTCoub_2AUogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
#     'H_BDCLCKID_SF': 'tR-qVIK5tIK3H48k-4QEbbQH-UnLqMPt22OZ04n-ah05SR-GhPosL4-hqHoytnT8X55x0J7m3UTKsq76Wh35K5tTQP6rLtbpBGb4KKJxbPbh8U7-j-5rDx_AhUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCDRe5LbDTjM-xQ0atcK2I6ysJoq2RbhKROvhjR4Wb0gyxomtjj0ymQl2MoH2UAWOTCGhTO0Dl_EbJtqLUkqKC8qVU7hyf5SM4tmLPcbXMT3QttjQTvufIkja-KELK_hsJ7TyU42hf47yhDL0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OhJRLDVC_yJKPhhDvPMCTBbJt_-U-X5-RLfbcR_p7F5l8-h43bqtQIXPLJhUn8e6QyJTLHoJcX-ROxOKQphTOkKqvbDp6T34QBMDc-QpbN3KJm_nL9bT3v5tD8K-QJ2-biWbRL2Mbdbj6P_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhhCGe6KbjjJyDa0jqbvWttoLBRrj-b7SKROvhjRb5JLgyxom2xvmQgvqaROH2n7of5CGhTO0DxPUDMJ9LUvQMgJu2bT_Lx7YVbTLehjkbfJBQttjQn3hfIkja-5t5b5bqb7TyU42bU47yaji0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OuJRLDVILyJC02MDvPKITD-tFO5eT22-usQm5R2hcHMPoosIOKb5oobjkJLPvatU3L3CO0XJvCBMbUotoHXnJi0btQDPvxBf7p5acuhp5TtUJMsJn2LPnh-lRXLJoyKMnitIv9-pPKWhQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKu-n5jHjJLjHLf3H',
#     'BDSFRCVID_BFESS': 'UIDOJexroG3Vd5oe8hCLb4DmEoizkVOTDYrEOwXPsp3LGJLVgVMXEG0PtEhTCoub_2AUogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
#     'H_BDCLCKID_SF_BFESS': 'tR-qVIK5tIK3H48k-4QEbbQH-UnLqMPt22OZ04n-ah05SR-GhPosL4-hqHoytnT8X55x0J7m3UTKsq76Wh35K5tTQP6rLtbpBGb4KKJxbPbh8U7-j-5rDx_AhUJiB5OMBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbCDRe5LbDTjM-xQ0atcK2I6ysJoq2RbhKROvhjR4Wb0gyxomtjj0ymQl2MoH2UAWOTCGhTO0Dl_EbJtqLUkqKC8qVU7hyf5SM4tmLPcbXMT3QttjQTvufIkja-KELK_hsJ7TyU42hf47yhDL0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OhJRLDVC_yJKPhhDvPMCTBbJt_-U-X5-RLfbcR_p7F5l8-h43bqtQIXPLJhUn8e6QyJTLHoJcX-ROxOKQphTOkKqvbDp6T34QBMDc-QpbN3KJm_nL9bT3v5tD8K-QJ2-biWbRL2Mbdbj6P_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhhCGe6KbjjJyDa0jqbvWttoLBRrj-b7SKROvhjRb5JLgyxom2xvmQgvqaROH2n7of5CGhTO0DxPUDMJ9LUvQMgJu2bT_Lx7YVbTLehjkbfJBQttjQn3hfIkja-5t5b5bqb7TyU42bU47yaji0q4Hb6b9BJcjfU5MSlcNLTjpQT8r5MDOK5OuJRLDVILyJC02MDvPKITD-tFO5eT22-usQm5R2hcHMPoosIOKb5oobjkJLPvatU3L3CO0XJvCBMbUotoHXnJi0btQDPvxBf7p5acuhp5TtUJMsJn2LPnh-lRXLJoyKMnitIv9-pPKWhQrh459XP68bTkA5bjZKxtq3mkjbPbDfn028DKu-n5jHjJLjHLf3H',
#     'Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925': '1614845791,1614851136,1614851240,1615165729',
#     'shitong_key_id': '2',
#     'H_PS_PSSID': '33356_33256_33273_33594_33570_33392_26350',
#     'delPer': '0',
#     'PSINO': '2',
#     'BA_HECTOR': '2k010la40l858k80d81g4augh0r',
#     'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
#     'BAIDUID_BFESS': '3F3F150D38D152315DC9909057892743:FG=1',
#     'ZD_ENTRY': 'empty',
#     'Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925': '1615166435',
#     'ab_sr': '1.0.0_NWRkYmE5YTFiOGFjZDFlYTA2MDUxZTE5OTIzYmM2YjhkMDcxZTg1NGY5MWU3MTExOGI0MWI2MWU0NzJlYjVlMzdhYTRmZTI4MWE2NTI4MmZlMDA4YmI4NGExZDc5ZTU3',
#     'shitong_data': 'dbdf29d6fefaba7fbe54a5f08c56473fe62657d4818cfc3475da5c754c9926a908d06f9c806606460150cd58de1501ba376c368ab857a5286deb46af0c0f6f1c7044d9f154873c8c22a38f3e06c83126aeb9682075d545d3b288b5d64eaeb651dfb772f3fc8622e1f36c47074bf7a727f59281bc8a3eb360b5b68cf0d6f83259',
#     'shitong_sign': 'e9a973dc',
# }
# keyWord = "停电|断电|偷电|限电|触电|跳闸|火灾|起火|失火|着火|爆炸|火花|线路|电线杆|线缆|电缆|电线|电力|电表箱|电塔|光纤|变压器|高压线|电网|充电桩|高压电线|电力设施|配电箱|变电站|国网|国家电网|供电局|电力局|供电公司|电厂|日立|电梯"
# keyWords = keyWord.split('|')
# site = "百度知道"
# for word in keyWords:
#     words = urllib.parse.quote(word)
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
#         'Referer': 'https://zhidao.baidu.com/search?word='+words+'&ie=gbk&site=-1&sites=0&date=2&pn=0',
#
#
#     }
#
#     params = (
#         ('word',word),
#     )
#     response = requests.get('https://zhidao.baidu.com/search', headers=headers, params=params, cookies=cookies)
#
#     #NB. Original query string below. It seems impossible to parse and
#     #reproduce query strings 100% accurately so the one below is given
#     #in case the reproduced version is not "correct".
#     # response = requests.get('https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word=%E5%81%9C%E7%94%B5', headers=headers, cookies=cookies)
#
#
#     #NB. Original query string below. It seems impossible to parse and
#     #reproduce query strings 100% accurately so the one below is given
#     #in case the reproduced version is not "correct".
#     # response = requests.get('https://zhidao.baidu.com/search?word=^%^E5^%^81^%^9C^%^E7^%^94^%^B5&ie=gbk&site=-1&sites=0&date=2&pn=0', headers=headers, cookies=cookies)
#
#
#     #NB. Original query string below. It seems impossible to parse and
#     #reproduce query strings 100% accurately so the one below is given
#     #in case the reproduced version is not "correct".
#     # response = requests.get('https://zhidao.baidu.com/search?word=^%^CD^%^A3^%^B5^%^E7^%^CD^%^A3^%^B5^%^E7&ie=gbk&site=-1&sites=0&date=0&pn=0', headers=headers, cookies=cookies)
#     content = response.content
#
#     url = re.compile('<dt class="dt[\s\S]*?"[\s\S]*?>[\s\S]*?<a href="(.*?)"[\s\S]*?>').findall(str(content))
#     for urls in url:
#
#      articleURL(urls,site)