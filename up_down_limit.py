# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import numpy as np
import pandas as pd
import datetime as dt
#from matplotlib import pyplot as plt
import tushare as ts

ts.set_token('e0bfed9150b8a4d1a6ad21f73319071c7dc41ae352b8f6173c2b28434407f16a')
idx=ts.Idx()

sh380=idx.IdxCons(ticker='000009').iloc[:,5:7]




df=pd.DataFrame(data=0,index=sh380.iloc[:,0],columns=['velocity'])
df['gain']=0
df['25pct']=0
df['75pct']=0
df['secShortName']=''

delta=60
today=dt.date.today()
begin_date=today -dt.timedelta(delta)
# hist = DataAPI.MktFunddGet(beginDate=begin_date,endDate=today,ticker = '510300',pandas="1")
# hist = DataAPI.MktEqudAdjGet(beginDate=begin_date,endDate=today,secID = universe,pandas="1") #field=[u'closePrice',u'secID',u'tradeDate'],
mkt=ts.Market()

for a in range(len(sh380)):

    # sec1=hist.sort_values('closePrice').reset_index(drop=True)
    
    sec1=mkt.MktEqud(beginDate=begin_date.strftime('%Y%m%d'),endDate=today.strftime('%Y%m%d'),ticker = str(sh380.iloc[a,1]))
    sec1=sec1.sort_values('closePrice').reset_index(drop=True)
       
    
    if len(sec1)<delta/2:
        continue
    sec_25pct=sec1.loc[len(sec1)/4,'closePrice']
    sec_50pct=sec1.loc[len(sec1)/2,'closePrice']
    sec_75pct=sec1.loc[len(sec1)*3/4,'closePrice']
    sec1=sec1.sort_values('tradeDate').reset_index(drop=True)

    df.iloc[a,2]=sec_25pct
    df.iloc[a,3]=sec_75pct
    df.iloc[a,4]=sec1.loc[0,'secShortName']
    velocity_count=0

    while True:

        #判断是否后面无下一个买卖点出现，如果是，将sec1设为空
        if len(sec1[sec1.closePrice<=sec_25pct])==0 and len(sec1[sec1.closePrice>=sec_75pct])==0:
            sec1 = []
            df.iloc[a,0]=velocity_count
            df.iloc[a,1]=velocity_count*(sec_75pct-sec_25pct)/sec_25pct
            break
        #找到下一个小于25%收盘价的记录
        call=sec1[sec1.closePrice<=sec_25pct].head(1).index


        if len(call )!=0:
            call = int(call.to_native_types()[0])
            sec1= sec1.loc[call:,:]
            put=sec1[sec1.closePrice>=sec_75pct].head(1).index

            if len(put)!=0:
                put = int(put.to_native_types()[0])
                sec1=sec1.loc[put:,:]
                velocity_count+=1
                # log.info('put if len sec1:'+str(len(sec1)))
            else:
                sec1 = []
                # log.info('put else len sec1:'+str(len(sec1)))
                df.iloc[a,0]=velocity_count
                df.iloc[a,1]=velocity_count*(sec_75pct-sec_25pct)/sec_25pct
                break 
        else:
            sec1=[]
            df.iloc[a,0]=velocity_count
            df.iloc[a,1]=velocity_count*(sec_75pct-sec_25pct)/sec_25pct

            # log.info('call else len sec1:'+str(len(sec1)))
            break


        
df.sort_values('gain').tail(10)



# n,bins, patches =plt.hist(hist.closePrice,10)
