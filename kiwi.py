import pandas as pd
import re
from lxml.html import urljoin
from lxml import etree
import requests
from time import sleep
from os import environ
from os.path import join

initialURL=['http://bbs.skykiwi.com/forum.php?mod=forumdisplay&fid=18&filter=typeid&typeid=472','http://bbs.skykiwi.com/forum.php?mod=forumdisplay&fid=18&filter=typeid&typeid=473','http://bbs.skykiwi.com/forum.php?mod=forumdisplay&fid=18&filter=typeid&typeid=474']


def ReadPost(url):
    res=requests.get(url)
    response=etree.HTML(res.text)
    details=response.xpath('//td[@class="td-title"]/text()|//td[@class="td-content"]/text()')
    df=pd.DataFrame(data=None, columns=['tid','年份', '制造商', '车辆型号', '车牌号码', '公里数', '变速箱','排气量','价格','内容','最后编辑'])
    if details==[]:
        return df
    details1=details[1:14:2]
    details1.insert(0,re.search(r'tid=\d+',res.url).group()[4:])
    if re.search(r'\d+',str(details[-1:])) is None:
        details1.append(0)
    else:
        details1.append(re.search(r'\d+',str(details[-1:])).group())
    details1[1]=int(re.search('\d+',details1[1]).group())
    details1[2]=re.match('\w+',details1[2]).group()
    details1[5]=re.match('\w+',details1[5]).group()
    

    # get 1st post
    postid=response.xpath('//td[@class="t_f"]/@id')[0]
    details1.append(' '.join(x.strip() for x in response.xpath('//td[@id="'+postid+'"]//text()')))
    # get last edit date
    # no price update
    if len(response.xpath('//i[@class="pstatus"]'))==0:
        # recent post or not
        if re.search('\d+-\d+-\d+',response.xpath('//em[contains(@id,"authorposton")]/text()|//em[contains(@id,"authorposton")]/span/@title')[0]) is None:
            details1.append(re.search('\d+-\d+-\d+',response.xpath('//em[contains(@id,"authorposton")]/text()|//em[contains(@id,"authorposton")]/span/@title')[1]).group())
        else:
            details1.append(re.search('\d+-\d+-\d+',response.xpath('//em[contains(@id,"authorposton")]/text()')[0]).group())
    else:
        details1.append(re.search('\d+-\d+-\d+',response.xpath('//i[@class="pstatus"]/text()')[0]).group())

    df1=pd.DataFrame(details1).T
    df1.columns=df.columns
    df=df.append(df1)
    return df

Result_df=pd.DataFrame(data=None, columns=['tid','年份', '制造商', '车辆型号', '车牌号码', '公里数', '变速箱','排气量','价格','内容','最后编辑'])

for cate in initialURL:

    res=requests.get(cate)
    response=etree.HTML(res.text)
    # all pages
    pages=response.xpath('//div[@class="pg"]/a[count(@class)=0]/@href')
    pages=pages[:int(len(pages)/2)]
    pages=list(map(lambda x:urljoin(res.url,x),pages))
    pages.insert(0,res.url)

    # all posts
    UrlList=[]
    for page in pages:
        res=requests.get(page)
        response=etree.HTML(res.text)
        UrlList=UrlList+response.xpath('//table/tbody[contains(@id,"normalthread")]/tr/th/a[1]/@href')
    UrlList=list(map(lambda x:urljoin(res.url,x),UrlList))

    for url in UrlList:
        # if len(Result_df)>0 and len(Result_df.loc(Result_df.tid==re.search('tid=\d+',url).group()[4:]))==1:
        #     continue
        Result_df=Result_df.append(ReadPost(url),ignore_index=True)
        sleep(10)





