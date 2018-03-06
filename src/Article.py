# -*- coding: utf-8 -*-

class Article:
    def __init__(self, title='', article='', date=None, has_keywords=False, tags=set(), sentences=[]):
        self.title = title
        self.article = article
        self.date = date
        self.has_keywords = has_keywords
        self.tags = tags

    def __str__(self):
        s = 'title: ' + self.title.encode('utf-8') + '\n'
        s += 'article: ' + self.article.encode('utf-8') + '\n'
        s += 'date: ' + str(self.date) + '\n'
        s += 'keywords:' + str(self.has_keywords) + '\n'
        s += 'tags: ' + str(self.tags) + '\n'
        return s

    def split_sentences(self):
        i = 0
        prev = ''
        sentences = []
        punct = set(',.!?:;~，。！？：；～… '.decode('utf-8'))
        for j, word in enumerate(self.article):
            if prev in punct:
                i = j
            elif word in punct:
                sentences.append(self.article[i:j])
                i = j

            prev = word

        if prev not in punct:
            sentences.append(self.article[i:])

        return sentences
