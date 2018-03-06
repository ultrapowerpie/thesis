# -*- coding: utf-8 -*- 

import codecs, os

with codecs.open('Remin_Ribao_utf8.txt', 'rb', encoding='utf-8') as f:
	text = f.read()

article_list = text.split('<REC>')

i = 0
for article in article_list[1:]:	
	s = article.find('<正标题>='.decode('utf-8'))+6
	t = min(article.find('\n', s), s+32)
	title = article[s:t].replace('/',' ')	

	date = article.find('<日期>='.decode('utf-8'))+5
	year = article[date:date+4]
	month = article[date+5:date+7]
	day = article[date+8:date+10]
	
	print (', '.join((str(i),year,month,day,title))).encode('utf-8')	

	directory = 'data/'+year+'/'+month+'/'+day+'/'

	if not os.path.exists(directory):
		os.makedirs(directory)	
	
	with open(directory+'/'+title, 'wb') as f:
		f.write(article.encode('utf-8'))

	i += 1
