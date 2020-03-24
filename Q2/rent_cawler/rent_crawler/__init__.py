__ALL__ = ['main']
from itertools import chain
from rent_crawler.crawlers import get_searchUrlist,get_house
from rent_crawler.config.headers import user_agent_list
from rent_crawler.config.region_map import region_map
import random
import requests


def main(**kwargs):
    client = requests.session()
    SOURCES = kwargs.get('sources')
    headers = dict()
    headers['user-agent'] = random.choice(user_agent_list)
    if 'all' in SOURCES:
        print('run all')
        crawlerList = [get_searchUrlist(client,key,headers) for key in region_map.keys()]
    else:
        crawlerList_v1 = []
        for src in SOURCES:
            if src in region_map:
                print('run ' + src + '...')
                crawlerList_v1.extend(get_searchUrlist(client,src,headers))


    # # print(crawlerList_v1)
    crawlerList = crawlerList_v1
    data_info = get_house(crawlerList, headers)
    print(data_info[-1])
    print(len(data_info))
