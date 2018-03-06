# -*- coding: utf-8 -*-
import math
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from Aggregator import Aggregator


class Plot:
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    yearsFmt = mdates.DateFormatter('%Y')

    def __init__(self, dataset, delimiter='-'):
        self.dataset = dataset
        self.n = int(math.sqrt(len(dataset))) + 1
        self.fig = plt.figure()
        self.plot_timeseries(delimiter)
        plt.show()

    def plot_timeseries(self, delimiter):
        for i, (key, val) in enumerate(self.dataset.items()):
            subplt = self.fig.add_subplot(self.n, self.n, i + 1)
            x, y = zip(*val)
            subplt.plot_date(x, y, xdate=True, marker=None, ls='solid')

            funcs, keywords, tags = key.split(delimiter)
            s_func, a_func, c_func = funcs.split(',')
            tags = tags.split(',')
            title = 'Sentence AggFunc: ' + s_func + '\n'
            title += 'Article AggFunc: ' + a_func + '\n'
            title += 'Coalesce Func: ' + c_func + '\n'
            title += 'Has Keywords: ' + keywords + '\n'
            title += '   Article Tag: ' + tags[0]
            title += '   Sentence Tag:' + tags[1]
            subplt.title.set_text(title)

            subplt.format_xdata = mdates.DateFormatter('%Y-%m-%d')
            subplt.xaxis.set_major_locator(self.years)
            subplt.xaxis.set_major_formatter(self.yearsFmt)
            subplt.xaxis.set_minor_locator(self.months)
            # subplt.grid(color='b', linestyle='-', linewidth=0.1, which='minor')


if __name__ == '__main__':
    filename = '../data/sentiment_data.txt'
    US = '美国'.decode('utf-8')
    agg = Aggregator(filename, True, US, US)
    Plot(agg.get_aggs())
