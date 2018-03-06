import codecs

with codecs.open('/opt/datafeed/Renmin Ribao 2001-2012.txt', 'rb', encoding='GB2312', errors='ignore') as f:
    binary = f.read()

with open('Remin_Ribao_utf8.txt', 'wb') as f:
    f.write(binary.encode('utf-8'))	
