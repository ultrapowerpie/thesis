# 人民日报 (People's Daily) Sentiment Analysis Tools

## Required packages
- python 2.7
- numpy
- [jieba](https://github.com/fxsjy/jieba)

## References
- Article texts accessed from the [Green Apple Data Center](www.egreenapple.com)
- Sentiment analysis code adapted from [SentimentCN](https://github.com/data-science-lab/sentimentCN)

## Configuration
- Configuration of both the search tool and sentiment aggregator tools can be
found in config.ini

## Tools

### Search Tool
The search tool (search.py) uses python's standard regex matching to count the
number of appearances a given regex serach term appears in the dataset,
aggregated by summation over a window of the given number of days. Both raw
search term counts and article counts are provided (the
number of articles containing the search term).

### Sentiment Aggregator Tool
The aggregator tool aggregates the sentiment of articles matching the specified
filters (set in configuration file), and aggregates by summation over a window
of the given number of days.

The SentimentCN tools compute both positive and negative sentiment scores at
the sentence level for simplified Chinese. Aggregated values of both sum of
positive and negative and just negative sentiment score of each sentence are
given. Both values are aggregated by summation over sentences within each
article as well as values averaged (mean) over sentences within each articles.
Values are summed over all articles in each window, but article counts are given
if mean article sentiment values are desired.
