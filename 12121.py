import requests

cookies = {
    'tt_dsid': 'fdasof09vni234NGVjMGNhNWQwOTk0ZjQ5NGEzZmRlMzA2YTU5MmI3YTI=',
    'xxl_city_code': 'local_BeiJing',
    'notFoundUid': '4w7udgau50rhumjo4tsskt84qr70sptk',
    'xxl_hdr_info': 'MjIxLjIxNy4xMDcuMTY2',
    'xxl_hdr_data': '5rW35reA5Yy6fOa4heays+ihl+mBk3zmuIXmsrN85riF5rKz5q+b57q66LevMTblj7fpmaJ8',
    '__guid': '94825664.2523075927667669000.1615889938105.5842',
    'stc_mlook_tsl': 'U6X_RzSoWkYX',
    'count': '3',
    'monitor_count': '3',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
}

params = (
    ('callback', 'jQuery19108678869398415983_1615887565219'),
    ('url', '99ab0188bed7661e2'),
)

response = requests.get('https://m.look.360.cn/transcoding', headers=headers, params=params, cookies=cookies)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://m.look.360.cn/transcoding?callback=jQuery19108678869398415983_1615887565219&url=99ab0188bed7661e2', headers=headers, cookies=cookies)
print(response.content.decode("utf-8"))