# -*- coding: utf-8 -*-

import pandas as pd 
from time import sleep
import requests
import schedule
import datetime
import json


def checkDate(year,month,day):
    try:
        newDataStr="%04d/%02d/%02d"%(year,month,day)
        newDate=datetime.datetime.strptime(newDataStr,"%Y/%m/%d")
        return True
    except ValueError:
        return False
    
"""
task関数
現在のBTCの値を取得する
"""
def task():
    
    endPoint = 'https://api.coin.z.com/public'
    path     = '/v1/ticker?symbol=BTC'
    response = requests.get(endPoint + path)
    df = pd.json_normalize(response.json(),record_path='data')
    print("Get BTC rate...")
    print(df)
    return df
    
"""
past_task関数
過去のBTCの値を取得する
"""    

def past_task(year,month,day,interval,symbol):
    
    
    endPoint = 'https://api.coin.z.com/public'
    
    if day < 10:
        day = '0'+str(day)
    if month < 10:
        month = '0'+str(month)
        
    time = str(year)+str(month)+str(day)
    path     = '/v1/klines?symbol='+symbol+'&interval='+interval+'&date='+time
    response = requests.get(endPoint + path)
    df = pd.json_normalize(response.json(),record_path='data')
    print(str(year)+'-' + str(month) +'-' + str(day) +' get date of ' +symbol)
    return df
    
"""
ここから実行
"""  
start_date = datetime.date(2021, 4, 15)
flag = False 
symbol= 'BTC'

for i in range(2021,2023):
    for j in range (1,13):
        for k in range (1,32):            
            if flag:
                if checkDate(i,j,k):
                    if datetime.date(i, j, k) == datetime.date.today():
                        break
                    df = pd.concat([df,past_task(i,j,k,'1min',symbol)])                                    
            else:
                if checkDate(i,j,k):
                    if start_date == datetime.date(i, j, k):
                        df = past_task(i,j,k,'1min',symbol)
                        flag = True
            

df.to_csv(symbol+"_data.csv")                   
                        
                        
                        
            
            