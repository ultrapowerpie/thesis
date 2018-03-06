# -*- coding: utf-8 -*-

import codecs, datetime, pickle, re
from src.Article import Article
from src.SentimentCN import SentimentCN as SCN

ARTICLE_DELIM = '<REC>'.decode('utf-8')
TITLE_DELIM = '<正标题>='.decode('utf-8')
DATE_DELIM = '<日期>='.decode('utf-8')

MAX_TITLE_LEN = 32

US = '美国'.decode('utf-8')
TW = '台湾'.decode('utf-8')
SK = '韩国'.decode('utf-8')
NK = '朝鲜'.decode('utf-8')
JP = '日本'.decode('utf-8')

IR = '国际关系'.decode('utf-8')

KEYWORDS = {
    '国外'.decode('utf-8'),
    '外交'.decode('utf-8'),
    '对外'.decode('utf-8'),
    '国际'.decode('utf-8')
}


class Dataset:
    def __init__(self, load_path, data_path=None):
        self.taglist = [US, TW, SK, NK, JP]
        self.retags = re.compile('|'.join(self.taglist))
        self.rekws = re.compile('|'.join(KEYWORDS))

        if data_path:
            self.articles = self.build_dataset(load_path, data_path)

        with open(load_path, 'rb') as f:
            self.articles = pickle.load(f)

    def __len__(self):
        return len(self.articles)

    def add_article(self, article):
        self.articles.append(article)

    def get_articles(self):
        return self.articles

    def get_tags(self, text):
        return set(self.retags.findall(text))

    def has_keywords(self, text):
        return bool(self.rekws.match(text))

    def filter_articles(self, has_keywords=False, tags=None, start_date=None, end_date=None):
        if not tags:
            tags = set()

        if not start_date:
            start_date = datetime.date(datetime.MINYEAR, 1, 1)

        if not end_date:
            end_date = datetime.date(datetime.MAXYEAR, 12, 31)

        filtered_articles = []
        for article in self.articles:
            if has_keywords and not article.has_keywords:
                continue
            if tags.issubset(article.tags) and start_date <= article.date <= end_date:
                filtered_articles.append(article)

        return filtered_articles


    def search_articles(self, search_term):
        regex = re.compile(search_term)

        results = list(map(lambda a: [a.date, len(regex.findall(a.article))], self.articles))

        return list(filter(lambda x: x[1] > 0, results))


    def build_dataset(self, write_path, read_path, encoding='utf-8'):
        with codecs.open(read_path, 'rb', encoding=encoding) as f:
            text = f.read()

        article_list = text.split(ARTICLE_DELIM)

        dataset = []
        for i, article in enumerate(article_list[1:]):
            s = article.find(TITLE_DELIM) + len(TITLE_DELIM)
            t = min(article.find('\n', s), s + MAX_TITLE_LEN)
            title = article[s:t].replace('/', ' ')

            date = article.find(DATE_DELIM) + len(DATE_DELIM)
            year = int(article[date:date + 4])
            month = int(article[date + 5:date + 7])
            day = int(article[date + 8:date + 10])

            date = datetime.date(year, month, day)

            tags = self.get_tags(article)
            has_keywords = self.has_keywords(article)

            dataset.append(Article(title, article, date, has_keywords, tags))

            print (', '.join((str(i), str(date), title))).encode('utf-8')

        with open(write_path, 'wb') as f:
            pickle.dump(dataset, f)

        return dataset

    def build_sentiment_dataset(self, scn_path, write_path):
        scn = SCN(scn_path)

        with open(write_path, 'wb') as f:
            for i, a in enumerate(self.articles):
                s = 'ARTICLE\n'
                s += str(a.date) + '\n'
                s += str(a.has_keywords) + '\n'
                s += ' '.join(a.tags) + '\n'

                for sent in a.split_sentences():
                    p, n = scn.sentiment_score(sent)
                    s += ' '.join(self.get_tags(sent)) + '\t' + str(p) + ' ' + str(n) + '\n'

                f.write(s.encode('utf8'))

                print i
