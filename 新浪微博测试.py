import requests

headers = {

    'cookie': 'SINAGLOBAL=528688026201.6336.1613962949023; SSOLoginState=1615280776; XSRF-TOKEN=FIhLqmY14zaRGoc7fjSJXaoS; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWymNhhY0SzjnBEUszxE-S45JpX5KMhUgL.FoqcSK-NeoepShM2dJLoIfQLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1KeLBKqLxK-L1K2L1h5t; ALF=1647023312; SCF=ApM_kj7Dez93SnOvW5JWvXPR1nRXpfshE-RxvP3v0UrRWIPQHCiN5fW75ySTPAwX1pFYWbF5Gjo8KCX6m51HY2o.; SUB=_2A25NThEBDeRhGeBI7lcW8i3NzzuIHXVuOgXJrDV8PUNbmtAKLULikW9NRpWnaBTbyww7UmFtF5BjncmkthV92Bee; WBPSESS=rqSHduCmTE6mwR3AmolJkl1XkzTcvYH5iTl5vDV377tzWdyVkvFowRa5ozrB8wZpJGjy0Ws3Oi_ROWZ61hyVLHYluc6wwsPDRD39FU9JcT6Wa8Ope9fp5yxn5xZzchIQ; TC-V-WEIBO-G0=35846f552801987f8c1e8f7cec0e2230; _s_tentry=-; Apache=2893262158942.0024.1615532004844; ULV=1615532004936:3:1:1:2893262158942.0024.1615532004844:1614239633185',
}

params = (
    ('id', 'K48eEa5Vk'),
)

response = requests.get('https://weibo.com/ajax/statuses/longtext', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://weibo.com/ajax/statuses/longtext?id=K48eEa5Vk', headers=headers)
print(response.content.decode("utf-8"))