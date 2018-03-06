# -*- coding: utf-8 -*-

from datetime import datetime as dt
import numpy as np
from collections import defaultdict as dd
from matplotlib import dates as mdates


class Aggregator:

    MYDICT = {
        '美国'.decode('utf-8'): 'US',
        '台湾'.decode('utf-8'): 'TW',
        '韩国'.decode('utf-8'): 'SK',
        '朝鲜'.decode('utf-8'): 'NK',
        '日本'.decode('utf-8'): 'JP'
    }

    AGG_FUNCS = {
        'SUM':np.sum,
        'MEAN':np.mean,
    }

    def __init__(self, filename, has_keywords=None, article_tag=None, sentence_tag=None):
        self.filename = filename
        self.has_keywords = has_keywords
        self.article_tag = article_tag
        self.sentence_tag = sentence_tag

        self.agged_map = {}
        for s_name, s_func in self.AGG_FUNCS.items():
            self.article_map = self.agg_articles(s_func)
            for a_name, a_func in self.AGG_FUNCS.items():
                for c_func in ['SUM', 'NEG']:
                    title = ','.join([s_name, a_name, c_func]) + '-'
                    title += str(has_keywords) + '-'
                    title += ','.join([self.MYDICT[article_tag], self.MYDICT[sentence_tag]])

                    self.agged_map[title] = self.agg_months(a_func, c_func)

        title = ',,COUNT-'
        title += str(has_keywords) + '-'
        title += ','.join([self.MYDICT[article_tag], self.MYDICT[sentence_tag]])

        self.agged_map[title] = self.agg_months(None, 'COUNT')

    def get_aggs(self):
        return self.agged_map

    def agg_articles(self, agg_func):
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
                    date = mdates.date2num(dt.strptime(line, '%Y-%m-%d\n'))
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

    def agg_months(self, agg_func, coalesce_func):
        month_agg = []
        for date, vals in self.article_map.items():
            pos, neg = zip(*vals)

            if coalesce_func == 'SUM':
                agg = agg_func(pos) - agg_func(neg)

            elif coalesce_func == 'NEG':
                agg = agg_func(neg)

            elif coalesce_func == 'COUNT':
                agg = len(pos)

            month_agg.append([date, agg])

        return sorted(month_agg, key=lambda x: x[0])

