# # 爬取文章标题，发表时间，文章来源,作者，文章内容
#
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# import requests
# requests = requests.session();
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
# url = "http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/s5987/202101/t20210105_508744.html"   #打开字符串的url
# rsp = requests.get(url, headers=headers)
# rsp.encoding = 'utf-8'
# soup = BeautifulSoup(rsp.text,"html.parser")  #使用指定解析器解析获得链接内容
#
# head = soup.select("h1")[0].text  #获取文章标题
# date = soup.select(".moe-detail-shuxing")[0].text        #获取日期
# #source = soup.select(".source")[0].text    #获取来源
# article = soup.select("div.TRS_Editor p")[:-1]
#
# article = []        #定义列表
# for p in soup.select("div.TRS_Editor p")[:-1]:    #获得每段内容
#     article.append(p.text.strip())          #追加至列表里
# article = '\n\n'.join(article)              #每段两个换行，为看起来方便
# # article = '\n\n'.join([p.text.strip() for p in soup.select("#article p")[:-1]])     #Python的一行烩
#              #获取文章的内容
# dates = str(date)[0:10]
# souce = str(date)[14:]
# #author = soup.select(".TRS_Editor")[0].text.strip("")  #获取作者
# print(head, '=====',dates, '========',article, '======',souce)