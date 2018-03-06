# -*- coding: utf-8 -*-

import codecs, os
import pickle
import datetime
import time
import calendar

from collections import defaultdict as dd
from SentimentCN import SentimentCN as SCN
from Dataset import *
from Article import Article

dataset = Dataset('../static_data/article_data.pkl')

tags_list = [{US}, {JP}, {TW}, {SK}, set()]

for tags in tags_list:
    print 'KEYWORDS'
    print 'TRUE'
    print 'TAGS'
    print ','.join(tags).encode('utf8')
    for year in range(2001,2013):
        for month in range(1,13):
            start_date = datetime.date(year, month, 1)
            end_date = datetime.date(year, month, calendar.monthrange(year, month)[1])

            filtered_articles = dataset.filter_articles(has_keywords=True, tags=tags, start_date=start_date, end_date=end_date)

            print ' '.join([str(year), str(month), str(len(filtered_articles))]).encode('utf8')


for tags in tags_list:
    print 'KEYWORDS'
    print 'FALSE'
    print 'TAGS'
    print ','.join(tags).encode('utf8')
    for year in range(2001,2013):
        for month in range(1,13):
            start_date = datetime.date(year, month, 1)
            end_date = datetime.date(year, month, calendar.monthrange(year, month)[1])

            filtered_articles = dataset.filter_articles(tags=tags, start_date=start_date, end_date=end_date)

            print ' '.join([str(year), str(month), str(len(filtered_articles))]).encode('utf8')
