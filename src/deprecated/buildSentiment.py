# -*- coding: utf-8 -*-

import datetime, pickle

from Dataset import *
from Article import Article

# article_dataset = Dataset('../static_data/article_data.pkl', data_path='../static_data/Renmin_Ribao_utf8.txt')

article_dataset = Dataset('../static_data/article_data.pkl')

article_dataset.build_sentiment_dataset('../static_data/dict/', '../static_data/sentiment_data.txt')
