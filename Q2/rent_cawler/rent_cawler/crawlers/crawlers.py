from rent_crawler.config.region_map import region_map
from rent_crawler.config.headers import user_agent_list
from bs4 import BeautifulSoup as bs
from lxml import etree
from pprint import pprint
from pyquery import PyQuery as pq
from selenium import webdriver
from urllib.parse import urlencode
import json
import os
import pandas as pd
import re
import requests
import time

def get_var(region,headers):
	index_url='https://rent.591.com.tw/'
	client = requests.session()
	res = client.get(index_url,headers=headers)
	res.encoding = 'utf-8'
    res.cookies['urlJumpIp']=region_map[region]
    soup = bs(res.text, "lxml")

    totalRows = soup.select('#container > section.listBox > div > div.listLeft > div.page-limit > div > a.pageNext')[0]['data-total']
    CSRF_TOKEN = [i['content'] for i in soup.select('head > meta[\'name\']') if i['name']=="csrf-token"][0]
    return totalRows ,CSRF_TOKEN
    
def get_searchUrl(totalRows):
    params = {
        'is_new_list': 1,
        'type': 1,
        'kind':0,
        'searchtype':1,
        'region':region_map[region],
        'firstRow=':30,
        'totalRows':totalRows
    }
    base_url = 'https://rent.591.com.tw/home/search/rsList?'
    url = base_url + urlencode(params)
    return url