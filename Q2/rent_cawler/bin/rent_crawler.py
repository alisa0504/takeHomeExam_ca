#!/usr/bin/env python

import os
import sys

is_local = os.path.split(os.getcwd())[-1] == 'bin'
if is_local:
    print(f'Local execution {__file__}')
    from context import rent_crawler

from rent_crawler.cli import get_crawlerList

if __name__ == '__main__':
    if is_local:
        sys.exit(get_crawlerList('airport'))
    else:
        sys.exit(get_crawlerList())
