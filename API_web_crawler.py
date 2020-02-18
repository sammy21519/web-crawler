# This Python file uses the following encoding: utf-8
from bs4 import BeautifulSoup
import requests
import time
import xlwings as xw
import json
import os
from datetime import datetime
import numpy as np
import pandas as pd


# 輸入（第幾筆）資料，回傳該資料的時間、等級、最高浪高、最低浪高
def spot844_crawler (data_num):
    
    res = requests.get("http://magicseaweed.com/api/b4c578c145b856d43e9636279a5e50a7/forecast/?spot_id=844")
    data_json=res.json()  
        
    return {
        "localTimestamp" : data_json[(data_num)]["localTimestamp"],
        "rating" : data_json[(data_num)]["solidRating"],
        "max_swell" : data_json[(data_num)]["swell"]["maxBreakingHeight"],
        "min_swell" : data_json[(data_num)]["swell"]["minBreakingHeight"],
        "period" : data_json[(data_num)]["swell"]["components"]["combined"]["period"],
        "temperature" : data_json[(data_num)]["condition"]["temperature"],
    }
    
#開啟工作簿
wb = xw.Book(r"data_844.xlsx")
# 截取相對應的工作表
data_sheet = wb.sheets["工作表1"]
data_sheet.range("A5:G44").clear()

for data_num in range(0, 40):
    
    #呼叫函數
    data_844=spot844_crawler (data_num)
   
    # 偵測該工作表的最後一行行數
    last_row = data_sheet.range("A1").end("down").row
    
    #時間轉換成年/日/月/小時
    localTimestamp=data_844["localTimestamp"]
    localtime=datetime.fromtimestamp(localTimestamp)

    #寫入excel
    data_sheet.range(f"A{last_row+1}").value = localtime.strftime("%Y/%m/%d")
    data_sheet.range(f"B{last_row+1}").value = localtime.strftime("%H")  
    data_sheet.range(f"C{last_row+1}").value = data_844["rating"]
    data_sheet.range(f"D{last_row+1}").value = data_844["max_swell"]
    data_sheet.range(f"E{last_row+1}").value = data_844["min_swell"]
    data_sheet.range(f"F{last_row+1}").value = data_844["period"]
    data_sheet.range(f"G{last_row+1}").value = data_844["temperature"]
    
    

#製作報表

import numpy as np
import pandas as pd

#將白天時段過濾出來
df = data_sheet.range("A4").options(pd.DataFrame, expand="table").value
filter1=(df["時間"] < 18)
filter2=(df["時間"] > 4)
df_daytime=df[filter1 &filter2 ]

#取浪等前2高的row 寫入excel
report= df.groupby(by="日期").mean().sort_values(by="浪等", ascending=False)
report=report.round(decimals=1)
report=report [["浪等"]]
recom=report.iloc[[0, 1]]
data_sheet.range("K7").value = recom

#coding:utf-8 
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('qt5agg') 
from matplotlib.font_manager import * 

#定義自定義字體，文件名從1.b查看系統中文字體中來 
myfont = FontProperties(fname='/Users/sammyfile/opt/anaconda3/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf/SimHei.ttf') 
#解決負號'-'顯示為方塊的問題 
matplotlib.rcParams['axes.unicode_minus']=False 

#設定折線圖資料
df_6=df.set_index("時間")
rank=df_6["浪等"]*2
temp=df_6["氣溫"]
max_swell=df_6["浪最高"]
period=df_6["週期"]
time=[]
for t in range(3, 3*len(rank)+1, 3): 
    time.append(t)

#印出折線圖
plt.plot(time, rank, color = 'y', label='swell_rank', linestyle='--')
plt.plot(time, temp, color = 'r', label="temperature")
plt.plot(time, max_swell, color = 'b', label="max_swell")
plt.plot(time, period, color = 'g', linestyle='--', label="period")
plt.xlabel(u'hr')
plt.ylabel(u'°C / m ')
plt.title(u'六天浪況',fontproperties=myfont) 
plt.legend()

#儲存jpg檔
fig1 = plt.gcf()
plt.show()
fig1.savefig('pics/report_6d.jpg', dpi=100)
