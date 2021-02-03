import requests

headers = {
    # 'Connection': 'keep-alive',
    # 'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    # 'Accept': 'application/json, text/plain, */*',
    # 'sec-ch-ua-mobile': '?0',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    # 'Origin': 'https://www.9kd.com',
    # 'Sec-Fetch-Site': 'same-site',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
}

data = '{"firstId":0,"lastId":0,"limit":20,"page":1,"product":3,"tagId":0}'

response = requests.post('https://9kd.com/api/kd-content/contents/list/pc', headers=headers, data=data)

print(response.text)