# TechNewsAggregator

This project aggregates news articles from various sources, including:

* BBC 
* CNN
* Hacker News

It currently leverages the [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) library to parse the HTML content of news websites and extract relevant information.

## Testing ##

Run ```python -m pytest``` for the unit tests

The tests for individual news sources (test_fetch_bbc_top_articles, test_fetch_cnn_top_articles, and test_fetch_hacker_news_top_articles) are currently commented out. If you want to run tests for the specific sources, uncomment the corresponding tests in the test_news_scraper.py file and provide your own path.