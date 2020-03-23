__ALL__ = ['main']
from address_crawler.config.crawler_map import crawler_map
from address_crawler.config.headers import user_agent_list
from address_crawler.geocode import geocode
from address_crawler.geocode import get_location
from address_crawler.geocode import get_wikiData
from itertools import chain
import random


def get_geoLine(crawlerList, headers):
    data = get_location(crawlerList, headers)
    data_info = data[0]
    data_error = data[1]
    data_correct = get_wikiData(data_error)
    data_info = data_info + data_correct
    return data_info


def main(**kwargs):
    SOURCES = kwargs.get('sources')
    headers = dict()
    headers['user-agent'] = random.choice(user_agent_list)
    if 'all' in SOURCES:
        print('run all')
        crawlerList = [func(headers) for func in crawler_map.values()]
    else:
        crawlerList_v1 = []
        for src in SOURCES:
            if src in crawler_map:
                print('run ' + src + '...')
                crawlerList_v1.append(crawler_map[src])
        crawlerList_v2 = [func(headers) for func in crawlerList_v1]

    # print(crawlerList_v2)
    crawlerList = list(chain(*crawlerList_v2))
    data_info = get_geoLine(crawlerList, headers)
    print(data_info[-1])
    print(len(data_info))
