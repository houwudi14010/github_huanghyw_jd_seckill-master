import re

import requests
from bs4 import BeautifulSoup
ss = requests.Session()
import requests

import requests

headers = {
    'authority': 'www.toutiao.com',
    'sec-ch-ua': '^\\^Google',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.toutiao.com/',
    'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
    'cookie': 'tt_webid=6933028917298644488; ttcid=32890f64e2bd45d9bdfeeb9ee4ec0cb518; csrftoken=b2c81a019af6c16369885b0b51153f57; csrftoken=b2c81a019af6c16369885b0b51153f57; passport_csrf_token=f1a589923f6a47b3b050003572fbb873; s_v_web_id=verify_kn8a93df_MwhGt9hA_1q7n_4ppR_BFaJ_9qBJyQL3NqXb; _ga=GA1.2.1324346738.1617866055; ttwid=1^%^7CdnP8bdBsOz58NdS4IUPROLpz8sxMKcGfZDAm6W9LJnk^%^7C1618280477^%^7Cfb246ac1b7cb35b2550ec11c2ea333abb21310401c6769ccd5f54167ecaffb92; tt_webid=6940798089112831519; MONITOR_WEB_ID=cc904e5a-3087-486e-8337-4cc89bf03736; __ac_signature=_02B4Z6wo00f01uvWdygAAIDBWyeb4Khk1Irr8nOAANqQ6E2MdPP6UkS3FkD1d-peVU.WphIwZ8Fk3WxIZAoS-juiEbLIasvIdU25h9WFjVYVFv.JUKW2Pyb4BFySuxY9Ud08UzgXWVxml-6y8f; tt_scid=x5No5YYeVhDTsp21S4yr8kgIvpMV-PnJ3hnZR7NNSt1o6.vYhYR-fulDPxi56V260e6b',

}
hredss = {
    'cookie':'tt_webid=6933028917298644488; ttcid=32890f64e2bd45d9bdfeeb9ee4ec0cb518; csrftoken=b2c81a019af6c16369885b0b51153f57; csrftoken=b2c81a019af6c16369885b0b51153f57; passport_csrf_token=f1a589923f6a47b3b050003572fbb873; s_v_web_id=verify_kn8a93df_MwhGt9hA_1q7n_4ppR_BFaJ_9qBJyQL3NqXb; _ga=GA1.2.1324346738.1617866055; ttwid=1%7CdnP8bdBsOz58NdS4IUPROLpz8sxMKcGfZDAm6W9LJnk%7C1618280477%7Cfb246ac1b7cb35b2550ec11c2ea333abb21310401c6769ccd5f54167ecaffb92; tt_webid=6940798089112831519; MONITOR_WEB_ID=cc904e5a-3087-486e-8337-4cc89bf03736; __ac_nonce=06076b4da003759756599; __ac_signature=_02B4Z6wo00f01PqHF1wAAIDDSnb7lYqhn5D6oxPAAF7dfLjae4rjquyvXTwUIKiHNk-UHUdxnJ142xcsg5hmpBg2tkXeH-0wJoKw3XlcEB9jkdKUx1QuMtuuPW9unX5bTq8uVSSetnckltavbc; tt_scid=SPkoChujegTaahn471A7o.U97BdiAaKT0P0pdCGKuHfPKXnzeNi2r4BwX43E2StFa872'
}
params = (
    ('min_behot_time', '0'),
    ('category', '__all__'),
    ('utm_source', 'toutiao'),
    ('widen', '1'),
    ('tadrequire', 'true'),
    ('_signature', '_02B4Z6wo00f01E7aE7wAAIDD.iv.dIzVu6hO.hcAAHPH46JpIfqNatUpEpzGUXLtHYvTH9cMJ8P7dhHRK2BNAmtxuJ2vUqoEJhOu0gvlEZzxzTnYFfEodK1WTL9b6qKlSZ9bPFntKt4LrrA06d'),
)

response = ss.get('https://www.toutiao.com/api/pc/feed/', headers=headers, params=params)
contentUrl = response.content.decode("utf-8")
url = re.compile('"group_id": "(.*?)",').findall(str(contentUrl))
for i in url:
    articleUrl = "https://www.toutiao.com/a"+i
    response = ss.get(articleUrl, headers=hredss)
    content = response.content.decode("utf-8")
    bs = BeautifulSoup(response.text, 'html.parser')
    try:
        contents = bs.select("article")
        contents = contents[0].text
        title = re.compile("<title>(.*?)</title>").findall(str(content))
        title = title[0]
        a = re.compile('<div class="article-meta"><span>(.*?)</span><span>(.*?)</span></div>').findall(str(content))
        for t in a:
            souceUrl = t[0]
            pubTime = t[1]
            print(pubTime)
            print(souceUrl)
            print(title)
            print(contents)
    except Exception as err:
        pass