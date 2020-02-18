import numpy as np
import pandas as pd

#dataframe
df = data_sheet.range("A4").options(pd.DataFrame, expand="table").value
filter1=(df["time"] < 18)
filter2=(df["time"] > 4)
df_daytime=df[filter1 &filter2 ]

#find the top two ranking data 
report= df_daytime.groupby(by="data").mean().sort_values(by="rank", ascending=False)
report=report.round(decimals=1)
report=report [["rank"]]
recom=report.iloc[[0, 1]]
data_sheet.range("K7").value = recom

import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('qt5agg') 
from matplotlib.font_manager import * 


#set var for line chart
df_6d=df.set_index("time")
rank=df_6d["rank"]
temp=df_6d["temperature"]
max_swell=df_6d["max_height"]
period=df_6d["period"]
time=[]
#the data time is per 3 hour
for t in range(3, 3*len(rank)+1, 3): 
    time.append(t)

#line chart 
plt.plot(time, rank, color = 'y', label='swell_rank', linestyle='--')
plt.plot(time, temp, color = 'r', label="temperature")
plt.plot(time, max_swell, color = 'b', label="max_swell")
plt.plot(time, period, color = 'g', linestyle='--', label="period")
plt.xlabel(u'hr')
plt.ylabel(u'°C / m ')
plt.title(u'6 days swell forecast') 
plt.legend()

#save chart as file.jpg
fig1 = plt.gcf()
plt.show()
fig1.savefig('file.jpg', dpi=100)