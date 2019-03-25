def DownPingshu(StartNo,EndNo):
    from selenium import webdriver
    import requests
    from urllib.parse import unquote,urlsplit,urljoin
    from lxml import etree
    import re
    from time import sleep
    from random import randint
    
    InitialURL='http://www.pingshu8.com'
    if not (type(StartNo)==int and type(EndNo)==int):
        return print('missing parameters, expect two int input')
    URLlist=[]
    for each in range(StartNo,EndNo+1):
        URLlist.append(InitialURL+'/down_'+str(each)+'.html')

    ps8=requests.session()
    for each in URLlist:
        
        url=each
        ps8.get(url)
        headers={'Referer':url,'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
        response=etree.HTML(ps8.get(url).text)
        downurl=response.xpath('//script/text()')[0]
        downurl=unquote(unquote(downurl))
        downurl1=urljoin(InitialURL,re.search('bzmtv_Inc/download.asp\?fid=\d+&t=\d+',downurl).group())
        mp3=ps8.get(downurl1,headers=headers)
        FileName=urlsplit(unquote(mp3.url))[2]
        FileName='-'.join(FileName.split('/')[3:])
        print('downloaded '+FileName)
        sleep(randint(0,10))
        with open(FileName,'wb') as f:
            f.write(mp3.content)

