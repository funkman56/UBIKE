# -*- coding: utf-8 -*-
"""
Created on Wed May 22 16:50:20 2019

@author: 劉力豪
"""
import requests
import json
import sqlite3
import urllib3                  
urllib3.disable_warnings()                                                                              #刪除urllib3的警告訊息
while True :
    
    print("~"*20, "歡迎進入自行車租借查詢系統", "~"*20)
    selcity = input("新北市Ubike資訊 請按1\n桃園市Ubike資訊 請按2\n台南市Tbike資訊 請按3\n離開查詢系統    請按Enter\n>> ")
    print(""*2)
    
    if selcity == "1" :                                                                                 #新北市自行車
        
         conn = sqlite3.connect('opendatanewtaipei.db')
         sql = """ create table if not exists ubike(

                            id integer primary key autoincrement,
                            station varchar(50),
                            space int,
                            rent int
                                                   )
               """
         conn.execute(sql)
         url = "https://data.ntpc.gov.tw/od/data/api/54DDDC93-589C-4858-9C95-18B2046CC1FC?$format=json"
         response = json.loads(requests.get(url).text)
         for row in response :
             conn.execute("insert into ubike(station,space,rent) values('%s',%d,%d)" %(row['sna'],int(row['tot']),int(row['sbi'])))
         conn.commit()
         
         findstation = input("請輸入你想要搜尋的站名(ex 新店高中) : ")
         
         cursor = conn.execute("select * from ubike  where station = '{}'".format(findstation))          # 使用.format來帶入input的字串
         for x in cursor :
             print("站名: %s\n總停車格數: %d\n可借車輛數: %d\n可停空位數: %d" %( x[1],x[2],x[3],x[2]-x[3]))
         cursor = conn.execute("delete from ubike ")
         conn.commit()

         conn.close()
         
     
    elif selcity == "2" :                                                                               #桃園市自行車
        
         conn = sqlite3.connect('opendatataoyuan.db')
         sql = """ create table if not exists ubike(

                            id integer primary key autoincrement,
                            station varchar(50),
                            space int,
                            rent int
                                                   )
               """
         conn.execute(sql)
         url = "https://data.tycg.gov.tw/api/v1/rest/datastore/a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f?format=json"
         response = json.loads(requests.get(url,verify=False).text)                                    #要設定verify=False 否則會產生 SSL 錯誤(Max retries exceeded with url)
         
         for row in response['result']['records'] :                                                    #注意網頁中的格式，字典中的字典的值才是我爬的資訊    
             conn.execute("insert into ubike(station,space,rent) values('%s',%d,%d)" %(row['sna'],int(row['tot']),int(row['sbi'])))
         conn.commit()
         
         findstation = input("請輸入你想要搜尋的站名(ex 中央大學圖書館) : ")
         
         cursor = conn.execute("select * from ubike  where station = '{}'".format(findstation))          
         for x in cursor :
             print("站名: %s\n總停車格數: %d\n可借車輛數: %d\n可停空位數: %d" %( x[1],x[2],x[3],x[2]-x[3]))
         cursor = conn.execute("delete from ubike ")
         conn.commit()

         conn.close()
         
        
    
    
    elif selcity == "3" :                                                                             #台南市自行車
        
         conn = sqlite3.connect('opendatatainan.db')
         sql = """ create table if not exists ubike(

                            id integer primary key autoincrement,
                            station varchar(50),
                            space int,
                            rent int
                                                   )
               """
         conn.execute(sql)
         url = "http://tbike.tainan.gov.tw:8081/Service/StationStatus/Json"
         response = json.loads(requests.get(url).text)
         for row in response :
             conn.execute("insert into ubike(station,space,rent) values('%s',%d,%d)" %(row['StationName'],row['Capacity'],row['AvaliableBikeCount']))
         conn.commit()

         findstation = input("請輸入你想要搜尋的站名(ex 高鐵台南站) : ") 

         cursor = conn.execute("select * from ubike  where station = '{}' ".format(findstation))
         for x in cursor :
             print("站名: %s\n總停車格數: %d\n可借車輛數: %d\n可停空位數: %d" %( x[1],x[2],x[3],x[2]-x[3]))
         cursor = conn.execute("delete from ubike ")
         conn.commit()

         conn.close()
         
    elif selcity == "" :
        
         break
     
    else :
        
         print(""*2)
         print("無此選項 請重新輸入 !!")
         print(""*2)
         
    
