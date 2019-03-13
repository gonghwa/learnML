import pandas as pd
import re
from lxml.html import urljoin

initialURL=['http://bbs.skykiwi.com/forum.php?mod=forumdisplay&fid=18&filter=typeid&typeid=472','http://bbs.skykiwi.com/forum.php?mod=forumdisplay&fid=18&filter=typeid&typeid=473','http://bbs.skykiwi.com/forum.php?mod=forumdisplay&fid=18&filter=typeid&typeid=474']

fetch(initialURL[1])
UrlList=response.xpath('//table/tbody[contains(@id,"normalthread")]/tr/th/a/@href').extract()
url=response.urljoin(UrlList[0])
fetch(url)
details=response.xpath('//td[@class="td-title"]/text()|//td[@class="td-content"]/text()').extract()

details1=details[1:14:2]
details1.insert(0,re.search(r'tid=\d+',response.url).group()[4:])
details1.append(re.search(r'\d+',str(details[-1:])).group())
details1[2]=re.match('\w+',details1[2]).group()
df=pd.DataFrame(data=None, columns=['tid','年份', '制造商', '车辆型号', '车牌号码', '公里数', '变速箱','价格','内容'])

