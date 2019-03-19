import pandas as pd
import re
from lxml.html import urljoin
from lxml import etree
import requests

initialURL=['http://bbs.skykiwi.com/forum.php?mod=forumdisplay&fid=18&filter=typeid&typeid=472','http://bbs.skykiwi.com/forum.php?mod=forumdisplay&fid=18&filter=typeid&typeid=473','http://bbs.skykiwi.com/forum.php?mod=forumdisplay&fid=18&filter=typeid&typeid=474']


def ReadPost(url):
    res=requests.get(url)
    response=etree.HTML(res.text)
    details=response.xpath('//td[@class="td-title"]/text()|//td[@class="td-content"]/text()')

    details1=details[1:14:2]
    details1.insert(0,re.search(r'tid=\d+',res.url).group()[4:])
    details1.append(re.search(r'\d+',str(details[-1:])).group())
    details1[1]=int(details1[1])
    details1[2]=re.match('\w+',details1[2]).group()
    details1[5]=re.match('\w+',details1[5]).group()
    df=pd.DataFrame(data=None, columns=['tid','年份', '制造商', '车辆型号', '车牌号码', '公里数', '变速箱','排气量','价格','内容','最后编辑'])

    # get 1st post
    postid=response.xpath('//td[@class="t_f"]/@id')[0]
    details1.append(' '.join(x.strip() for x in response.xpath('//td[@id="'+postid+'"]//text()')))
    # get last edit date
    details1.append(re('\d+-\d+-\d+',response.xpath('//i[@class="pstatus"]').group()[0]))

    df1=pd.DataFrame(details1).T
    df1.columns=df.columns
    df=df.append(df1)
    return df


res=requests.get(initialURL[1])
response=etree.HTML(res.text)
urljoin(res.url,UrlList[0])


# all posts
UrlList=response.xpath('//table/tbody[contains(@id,"normalthread")]/tr/th/a/@href')
url=urljoin(res.url,UrlList[0])



# all pages
pages=response.xpath('//div[@class="pg"]/a[count(@class)=0]/@href')
pages=pages[:int(len(pages)/2)]
