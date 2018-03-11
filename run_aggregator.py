# -*- coding: utf-8 -*-
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from collections import defaultdict as dd
from src.Aggregator import Aggregator
from src.Dataset import *
import ConfigParser
import numpy as np

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

def running_sum(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    sums = cumsum[N:] - cumsum[:-N]
    return sums[::N]


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    section = 'AGGREGATOR'

    data_file = config.get(section, 'SENTIMENT_DATA_FILE')
    keywords = kw_map[config.get(section, 'KEYWORDS').lower()]
    article_tag = tag_map[config.get(section, 'ARTICLE_TAG').lower()]
    sentence_tag = tag_map[config.get(section, 'SENTENCE_TAG').lower()]
    window = int(config.get(section, 'WINDOW_SIZE'))
    output_file = config.get(section, 'OUTPUT_FILE')

    agg = Aggregator(data_file, keywords, article_tag, sentence_tag)

    aggs = agg.get_aggs()

    n = len(aggs)

    agg_map = dd(lambda: [0] * n)

    labels = [''] * n

    for i, (key, val) in enumerate(aggs.items()):
        x, y = zip(*val)
        labels[i] = key
        for j, date in enumerate(x):
            agg_map[date][i] = y[j]

    day_list = [[k] + v for k, v in agg_map.items()]
    day_list.sort(key=lambda x: x[0])

    zip_list = []
    for i, l in enumerate(zip(*day_list)):
        if i == 0:
            zip_list.append(l[window::window])
        else:
            zip_list.append(running_sum(l, window))

    agg_list = [['Dates'] + labels] + zip(*zip_list)

    string_list = [list(map(str, row)) for row in agg_list]

    tsv = ['\t'.join(row) for row in string_list]

    with codecs.open(output_file, 'wb', 'utf-8') as f:
        f.write('\n'.join(tsv))
