import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from collections import defaultdict as dd
from src.Dataset import Dataset
import ConfigParser
import datetime as dt
import numpy as np

START_DATE = dt.date(2001, 1, 1)
END_DATE = dt.date(2012, 12, 31)


def running_sum(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    sums = cumsum[N:] - cumsum[:-N]
    return sums[N::N]


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    section = 'SEARCH'

    data_file = config.get(section, 'ARTICLES_DATA_FILE')
    search_term = config.get(section, 'SEARCH_TERM').decode('utf8')
    window = int(config.get(section, 'WINDOW_SIZE'))
    output_file = config.get(section, 'OUTPUT_FILE')

    article_dataset = Dataset(data_file)

    filtered_articles = article_dataset.search_articles(search_term)

    counts_map = dd(lambda: [0, 0])

    for a in filtered_articles:
        date = a[0]
        articles, words = counts_map[date]
        counts_map[date] = [articles + 1, words + a[1]]

    delta = END_DATE - START_DATE
    for i in range(delta.days + 1):
        date = START_DATE + dt.timedelta(days=i)
        if date not in counts_map:
            counts_map[date] = [0, 0]

    counts = [[d, v[0], v[1]] for d, v in counts_map.items()]

    counts.sort(key=lambda x: x[0])

    dates, articles, counts = zip(*counts)
    dates = dates[window::window]
    conv_articles = running_sum(articles, window)
    conv_counts = running_sum(counts, window)
    agg_list = zip(dates, conv_articles, conv_counts)

    output = ['Date,Articles,Counts'] + [','.join(list(map(str, l))) for l in agg_list]

    with open(output_file, 'w') as f:
        f.write('\n'.join(output))