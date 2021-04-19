from urllib import request,error
import requests
import re
if __name__ == '__main__':
    agentUrl = "http://47.96.91.228:82/get/"
    res = requests.get(agentUrl)
    agenContent = res.content.decode("utf-8")
    dataip = re.compile('"proxy": "(.*?)",').findall(str(agenContent))
    ip = dataip[0]
    print(ip)

    # proxy_handler = request.ProxyHandler(proxy)
    # opener = request.build_opener(proxy_handler)
    # request.install_opener(opener)
    # try:
    #     rsp = request.urlopen(url)
    #     print(rsp)
    # except error.URLError as e:
    #     print(e)
    # except Exception as e:
    #     print(e)
