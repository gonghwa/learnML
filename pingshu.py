import requests
import re
from lxml import etree
from urllib.parse import unquote
from urllib.parse import urljoin

ps8=requests.session()
url='http://www.pingshu8.com/down_207592.html'
ps8.get(url)
headers={'Referer':url,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}

response=etree.HTML(ps8.text)
response=etree.HTML(ps8.get(url).text)
downurl=response.xpath('//script/text()')[0]
downurl=unquote(unquote(downurl))
downurl1=urljoin(url,re.search('bzmtv_Inc/download.asp\?fid=\d+&t=\d+',downurl).group())
r=ps8.get(downurl1,headers=headers)
filename=unquote(r.url)
