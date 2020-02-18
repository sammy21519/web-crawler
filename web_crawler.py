# This Python file uses the following encoding: utf-8
from bs4 import BeautifulSoup
import requests
import time
import json
import os
from datetime import datetime



# return a dictionary of wanted info
def web_crawler (data_num):
    
    res = requests.get("given_api_by_magicseaweed"")
    data_json=res.json()  
        
    return {
        "localTimestamp" : data_json[(data_num)]["localTimestamp"],
        "rating" : data_json[(data_num)]["solidRating"],
        "max_swell" : data_json[(data_num)]["swell"]["maxBreakingHeight"],
        "min_swell" : data_json[(data_num)]["swell"]["minBreakingHeight"],
        "period" : data_json[(data_num)]["swell"]["components"]["combined"]["period"],
        "temperature" : data_json[(data_num)]["condition"]["temperature"],
    }
