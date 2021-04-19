import requests

headers = {
    'authority': 'weibo.com',
    'sec-ch-ua': '^\\^Google',
    'accept': 'application/json, text/plain, */*',
    'x-xsrf-token': 'pkWRY1tFa1un5Sy7KlQrH-6D',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://weibo.com/u/2828741892',
    'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
}
old_cookies={
    'cookie': 'SINAGLOBAL=528688026201.6336.1613962949023; UOR=,,login.sina.com.cn; ULV=1616133981225:5:3:2:3463223176561.0054.1616133981215:1615965942520; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWymNhhY0SzjnBEUszxE-S45JpX5KMhUgL.FoqcSK-NeoepShM2dJLoIfQLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1K2L1h5t; ALF=1647911715; SSOLoginState=1616375715; SCF=ApM_kj7Dez93SnOvW5JWvXPR1nRXpfshE-RxvP3v0UrRqhxVClO7WSNdtkGPAvp4i6AesxBG-i6IZsH3SiHiwkc.; SUB=_2A25NU5_zDeRhGeBI7lcW8i3NzzuIHXVuKPY7rDV8PUNbmtAKLRKtkW9NRpWnaEw_9eQFCxmA-Kj-L7S5iO-4FKis; XSRF-TOKEN=pkWRY1tFa1un5Sy7KlQrH-6D; WBPSESS=rqSHduCmTE6mwR3AmolJkl1XkzTcvYH5iTl5vDV377vqpqpzVKQ0_RkbviGlzfyOGs_hf95WZzQIQaoHCc9PhNobuXh5nHLeCrQRfStajMzhk4p-4sw3YDiOml86VRMT',
}
params = (
    ('uid', '2828741892'),
    ('page', '1'),
    ('feature', '0'),
)

response = requests.get('https://weibo.com/ajax/statuses/mymblog', headers=headers, params=params,cookies=old_cookies)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://weibo.com/ajax/statuses/mymblog?uid=2828741892&page=1&feature=0', headers=headers)
new_cookies = response.cookies

print(response.content.decode("utf-8"))
print("111")
print(new_cookies)