# -*- coding: utf-8 -*-

import datetime as dt
import numpy as np
from collections import defaultdict as dd


class Aggregator:
    START_DATE = dt.date(2001, 1, 1)
    END_DATE = dt.date(2012, 12, 31)

    MYDICT = {
        '美国'.decode('utf-8'): 'US',
        '台湾'.decode('utf-8'): 'TW',
        '韩国'.decode('utf-8'): 'SK',
        '朝鲜'.decode('utf-8'): 'NK',
        '日本'.decode('utf-8'): 'JP',
        None:'None'
    }

    AGG_FUNCS = {
        'SUM': np.sum,
        'MEAN': np.mean,
    }

    COALESCE_FUNCS = {
        'SUM': lambda x: sum(x[0]) - sum(x[1]),
        'NEG': lambda x: -sum(x[1]),
        'COUNT': lambda x: len(x[0])
    }

    def __init__(self, filename, has_keywords=None, article_tag=None, sentence_tag=None):
        self.filename = filename
        self.has_keywords = has_keywords
        self.article_tag = article_tag
        self.sentence_tag = sentence_tag
        a_tag = self.MYDICT[article_tag]
        s_tag = self.MYDICT[article_tag]

        self.agged_map = {}
        for s_name, s_func in self.AGG_FUNCS.items():
            self.article_map = self.agg_sentences(s_func)
            for c_name in ['SUM', 'NEG']:
                title = ','.join([s_name, c_name, str(has_keywords), a_tag, s_tag])
                self.agged_map[title] = self.agg_articles(self.COALESCE_FUNCS[c_name])

        title = ','.join(['None', 'COUNT', str(has_keywords), a_tag, s_tag])
        self.agged_map[title] = self.agg_articles(self.COALESCE_FUNCS['COUNT'])

    def get_aggs(self):
        return self.agged_map

    def agg_sentences(self, agg_func):
        article_agg = dd(list)
        with open(self.filename, 'rb') as f:
            is_keywords = None
            is_tags = False
            is_date = False
            skip_article = False
            date = None
            for line in f:
                if skip_article:
                    if 'ARTICLE' in line:
                        is_date = True
                        skip_article = False
                    continue

                if is_date:
                    date = dt.datetime.strptime(line, '%Y-%m-%d\n').date()
                    is_date = False
                    is_keywords = True

                elif is_keywords:
                    if self.has_keywords is not None:
                        if bool('True' in line) != self.has_keywords:
                            skip_article = True
                            continue
                    is_keywords = False
                    is_tags = True

                elif is_tags:
                    if self.article_tag and self.article_tag not in line.decode('utf8'):
                        skip_article = True
                        continue

                    is_tags = False
                    agg = [[], []]

                else:
                    if 'ARTICLE' in line:
                        is_date = True
                        if date:
                            article_agg[date].append(map(agg_func, agg))
                        continue

                    s_tags, score = line.split('\t')

                    if self.sentence_tag and self.sentence_tag not in s_tags.decode('utf8'):
                        continue

                    pos, neg = score.split()
                    agg[0].append(float(pos))
                    agg[1].append(float(neg))

        return article_agg

    def agg_articles(self, coalesce_func):
        article_agg = []
        for date, vals in self.article_map.items():
            agg = coalesce_func(zip(*vals))
            article_agg.append([date, agg])

        delta = self.END_DATE - self.START_DATE
        for i in range(delta.days + 1):
            date = self.START_DATE + dt.timedelta(days=i)
            if date not in self.article_map:
                article_agg.append([date, 0])

        return sorted(article_agg, key=lambda x: x[0])
