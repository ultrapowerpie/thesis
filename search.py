import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from collections import defaultdict as dd
from src.Dataset import Dataset

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Missing arguments'

    if len(sys.argv) > 3:
        print 'Too many arguments'

    article_dataset = Dataset('static_data/article_data.pkl')

    search_term = sys.argv[1].decode('utf8')

    filtered_articles = article_dataset.search_articles(search_term)

    counts_map = dd(lambda: [0, 0])

    for a in filtered_articles:
        date = str(a[0])
        articles, words = counts_map[date]
        counts_map[date] = [articles + 1, words + a[1]]

    headers = ['Date,Articles,Counts']

    counts = [','.join([d, str(v[0]), str(v[1])]) for d, v in counts_map.items()]

    counts = [headers] + counts

    with open(sys.argv[2], 'w') as f:
        f.write('\n'.join(counts))
