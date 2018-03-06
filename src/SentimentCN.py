# -*- coding: utf-8 -*- 

import codecs
import jieba

from collections import defaultdict as dd

class SentimentCN:
	def __init__(self, path):
		self.path = path
		
		self.posdict = self.load_set("positive.txt")
		self.negdict = self.load_set("negative.txt")
		
		self.mostdict = self.load_set("most.txt")
		self.verydict = self.load_set("very.txt")
		self.moredict = self.load_set("more.txt")
		self.ishdict = self.load_set("ish.txt")	
		self.insuffdict = self.load_set("insufficient.txt")
		
		self.invdict = self.load_set("inverse.txt")
		
		self.worddict = dd(lambda:1.0)
		self.add_dict(self.mostdict, 4.0)
		self.add_dict(self.verydict, 3.0)
		self.add_dict(self.moredict, 2.0)
		self.add_dict(self.ishdict, 0.5)
		self.add_dict(self.insuffdict, 0.25)

	def load_set(self, filename):			
		with codecs.open(self.path+filename, 'rb', encoding='utf-8') as f:
			text = f.read()
		return set(text.splitlines())

	def add_dict(self, map_dict, val):
		for word in map_dict:
			self.worddict[word] = val

	def segment(self, sentence):
        	return list(jieba.cut(sentence))

	def sentiment_score(self, sentence):
		i = 0
		a = 0
		count = [[0,0,0],[0,0,0]]
		
		segment = self.segment(sentence)
		for word in segment:
			if word in self.posdict:
				flag = 0
			elif word in self.negdict:
				flag = 1
			else:
				i += 1
				continue

			count[flag][0] += 1
			parity = 0
		
			for w in segment[a:i]:
				if w in self.worddict:
					count[flag][0] *= self.worddict[w]
				if w in self.invdict:
					parity += 1
			
			if parity % 2 == 1: # odd
				count[flag][0] *= -1.0
				count[flag][1] += count[flag][0]
				count[flag][0] = 0
				count[flag][2] += count[flag][1]
				count[flag][1] = 0
			else:
				count[flag][2] = sum(count[flag])
				count[flag][0] = 0

			a = i + 1
               		i += 1

		pos_count = 0
		neg_count = 0
		if count[0][2] < 0 and count[1][2] > 0:
			neg_count += count[1][2] - count[0][2]
			pos_count = 0
		elif count[0][2] > 0 and count[1][2] < 0:
			pos_count = count[0][2] - count[1][2]
			neg_count = 0
		elif count[0][2] < 0 and count[1][2] < 0:
			neg_count = -count[0][2]
			pos_count = -count[1][2]
		else:
			pos_count = count[0][2]
			neg_count = count[1][2]

		return pos_count, neg_count

if __name__ == '__main__':
	text = '这款手机大小合适，配置也还可以，很好用，只是屏幕有点小。。。总之，戴妃+是一款值得购买的智能手机。'.decode('utf-8')

	scn = SentimentCN('../static_data/dict/')
	for s in scn.split_sentences(text):
		print s

	print scn.sentiment_score([text])
