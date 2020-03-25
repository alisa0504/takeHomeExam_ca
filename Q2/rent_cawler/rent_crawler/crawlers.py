from rent_crawler.config.headers import user_agent_list
from rent_crawler.config.region_map import region_map
from bs4 import BeautifulSoup as bs
from lxml import etree
from pprint import pprint
from urllib.parse import urlencode
import math
import json
import os
import pandas as pd
import re
import requests
import time

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
client = requests.session()

def get_var(client,region,headers):
    index_url='https://rent.591.com.tw/?kind=0&regionid='+region_map[region]
    res = client.get(index_url,headers=headers)
    res.encoding = 'utf-8'
    res.cookies['urlJumpIp']= region_map[region]
#     print(res.cookies.get_dict())
    soup = bs(res.text, "lxml")
#     print(soup.select('head > meta'))

    totalRows = soup.select('#container > section.listBox > div > div.listLeft > div.page-limit > div > a.pageNext')[0]['data-total']
    CSRF_TOKEN = [i['content'] for i in soup.select('head > meta[name]') if i['name']=="csrf-token"][0]
    return (totalRows ,CSRF_TOKEN)
    
def get_searchUrl(firstRow,region,headers):
    params = {
        'is_new_list': 1,
        'type': 1,
        'kind':0,
        'searchtype':1,
        'region':region_map[region],
        'firstRow':(firstRow*30),
        'totalRows':get_var(client,region,headers)[0]
    }
    base_url = 'https://rent.591.com.tw/home/search/rsList?'
    url = base_url + urlencode(params)
    return url

def get_searchUrlist(client,region,headers):
    vars = get_var(client,region,headers)
    headers['X-CSRF-Token'] = vars[1]
    times = math.floor(int(vars[0])/30) +1 if int(vars[0])%30 !=0 else math.floor(int(vars[0])/30)
    searchUrlist=[]
    for firstRow in range(times):
        searchUrl = get_searchUrl(firstRow,region,headers)
#         print(searchUrl)
        res_search = client.get(searchUrl,headers=headers)
        res_search.encoding = 'utf-8'
        data = json.loads(res_search.text)
#         print(data['data']['data'][0]['post_id'])
        rent_list = [[i['post_id'],i['region_name'],i['region_name']+' '+i['fulladdress'],'https://rent.591.com.tw/rent-detail-'+str(i['post_id'])+'.html'] for i in data['data']['data']]
#         print(rent_list[0])
        searchUrlist.extend(rent_list)     
    return searchUrlist

def get_house(searchUrl,headers):
    houses=[]
    for url in searchUrl:
        hid = url[0] 
        region = url[1]
        address = url[2] 
        detail_url = url[3]
        res_detail = requests.get(detail_url,headers=headers)
        soup_detail = bs(res_detail.text, "lxml")
        if "soup_detail.select('div.userInfo > div > span.kfCallName')[0]['data-name']" in locals():
            name = soup_detail.select('div.userInfo > div > span.kfCallName')[0]['data-name']
        if "soup_detail.select('div.userInfo > div > span.dialPhoneNum')[0]['data-value']" in locals():
            dialPhone = soup_detail.select('div.userInfo > div > span.dialPhoneNum')[0]['data-value']
        if  "soup_detail.select('div.userInfo > div > input#hid_tel')[0]['value']" in locals():
            hid_tel =  soup_detail.select('div.userInfo > div > input#hid_tel')[0]['value'] 
        if  "soup_detail.select('div.userInfo > div > input#hid_email')[0]['value']" in locals():
            hid_email = soup_detail.select('div.userInfo > div > input#hid_email')[0]['value']
        infs = [{j[0].text.replace(' ',''):j[1].text.replace(' ','').replace('：','') for j in  zip(i.select('div.one'),i.select('div.two'))} for i in soup_detail.select('ul.clearfix.labelList.labelList-1 > li')]
        attrs = [{''.join(i.text.split(':')[0].split()):''.join(i.text.split(':')[1].split()) } for i in soup_detail.select('ul.attr > li')]
        try:
            out_rec = {
                'hid' : hid,
                'region':region,
                'address': address,
                'name': name if "name" in locals() else None,
                'dialPhone' : dialPhone if "dialPhone" in locals() else None,
                'hid_tel' : hid_tel if "hid_tel" in locals() else None,
                'hid_email' : hid_email if "hid_email" in locals() else None,
                'price':soup_detail.select('div.price')[0].text.split('\n')[1],
                'url':detail_url
                
            }
            [out_rec.update(inf) for inf in infs]
            [out_rec.update(attr) for attr in attrs]
        except Exception as e:
            print(detail_url)
            print(e)
        houses.append(out_rec)
    return houses

