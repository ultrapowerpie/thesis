# -*- coding: utf-8 -*-
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from collections import defaultdict as dd
from matplotlib import dates as mdates
from src.Aggregator import Aggregator
from src.Dataset import *

if __name__ == '__main__':
    filename = 'data/sentiment_data.txt'

    if len(sys.argv) < 5:
        print 'Missing arguments'

    if len(sys.argv) > 5:
        print 'Too many arguments'

    kw_map = {
        'none': None,
        'true': True,
        'false': False
    }

    tag_map = {
        'us': '美国'.decode('utf-8'),
        'tw': '台湾'.decode('utf-8'),
        'sk': '韩国'.decode('utf-8'),
        'nk': '朝鲜'.decode('utf-8'),
        'jp': '日本'.decode('utf-8'),
        'none': None
    }

    KEYWORDS = {
        '国外'.decode('utf-8'),
        '外交'.decode('utf-8'),
        '对外'.decode('utf-8'),
        '国际'.decode('utf-8')
    }

    args = [a.lower() for a in sys.argv]

    agg = Aggregator(filename, kw_map[args[1]], tag_map[args[2]], tag_map[args[3]])

    aggs = agg.get_aggs()

    n = len(aggs)

    agg_map = dd(lambda: [0] * n)

    labels = [''] * n

    for i, (key, val) in enumerate(aggs.items()):
        x, y = zip(*val)
        labels[i] = key
        for j, date in enumerate(x):
            agg_map[date][i] = y[j]

    agg_list = [[mdates.num2date(k)] + v for k, v in agg_map.items()]

    agg_list = [['Dates'] + labels] + agg_list

    string_list = [list(map(str, row)) for row in agg_list]

    tsv = ['\t'.join(row) for row in string_list]

    with codecs.open(sys.argv[4], 'wb', 'utf-8') as f:
        f.write('\n'.join(tsv))
