import requests
import tld

r = requests.get('http://www.customs.gov.cn/customs/xwfb34/302425/index.html')



print (tld.get_tld(url, as_object=True).parsed_url.netloc)

