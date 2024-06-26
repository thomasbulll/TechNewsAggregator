# TechNewsAggregator

This project aggregates news articles from various sources, including:

* [BBC](https://www.bbc.co.uk/news/technology)
* [CNN](https://edition.cnn.com/business/tech)
* [Hacker News](https://news.ycombinator.com/)
* [Business Insider](https://www.businessinsider.com/tech)
* [Tech Crunch](https://techcrunch.com/)
* [Sky News](https://news.sky.com/technology/)
* [Wired](https://www.wired.co.uk/topic/technology/)
* [Venture Beat](https://venturebeat.com/)
* [Reddit](https://www.reddit.com)
    * [Technology](https://www.reddit.com/r/technology/)
    * [Tech News](https://www.reddit.com/r/technews/)
    * [Tech](https://www.reddit.com/r/tech/)
    * [Software](https://www.reddit.com/r/software/)
    
It currently leverages the [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) library to parse the HTML content of news websites and extract relevant information.

I also leverage the [Natural Language Toolkit](https://www.nltk.org/) for sentiment analysis on articles, in particular the [Vader](https://www.nltk.org/_modules/nltk/sentiment/vader.html) library.


## Testing ##

Run ```python -m pytest``` for the unit tests
