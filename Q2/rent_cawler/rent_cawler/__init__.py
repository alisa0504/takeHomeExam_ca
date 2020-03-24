__ALL__ = ['main']
from rent_crawler.config.region_map import region_map
from rent_crawler.config.headers import user_agent_list
from itertools import chain
import random


def main(**kwargs):
    SOURCES = kwargs.get('sources')
    headers = dict()
    headers['user-agent'] = random.choice(user_agent_list)
    if 'all' in SOURCES:
        print('run all')
        crawlerList = [func(headers) for func in region_map.values()]
    else:
        crawlerList_v1 = []
        for src in SOURCES:
            if src in region_map:
                print('run ' + src + '...')
                crawlerList_v1.append(region_map[src])
        crawlerList_v2 = [func(headers) for func in crawlerList_v1]

    # print(crawlerList_v2)
    crawlerList = list(chain(*crawlerList_v2))
    data_info = get_geoLine(crawlerList, headers)
    print(data_info[-1])
    print(len(data_info))
