import requests
import re
cookies = {

}

headers = {
    'Referer': 'https://www.thepaper.cn/',

}

response = requests.get('https://www.thepaper.cn/', headers=headers, cookies=cookies)
aa = response.content.decode("utf-8")
souce = re.compile('newsDetail_forward_(.*?)"').findall(str(aa))
print(souce)



