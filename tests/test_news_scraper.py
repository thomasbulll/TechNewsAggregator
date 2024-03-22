import sys
sys.path.append("..")
from news_scraper.aggregator import fetch_hacker_news_top_articles, fetch_bbc_top_articles, fetch_cnn_top_articles, fetch_parsed_html, fetch_tech_crunch_top_articles, fetch_business_insider_top_articles, fetch_sky_news_top_articles, fetch_wired_top_articles, fetch_venture_beat_top_articles, fetch_reddit_top_articles
from test_data.test_data_utl import retrive_test_file_directory
import pytest

# This test always passes under the assumption
# that google's homepage will never go down.
def test_fetch_parsed_html_success():
  first_url = "https://www.google.com/"
  first_soup = fetch_parsed_html(first_url)
  assert first_soup is not None

def test_fetch_parsed_html_failure():
  url = "test_invalid.html"
  soup = fetch_parsed_html(url)
  assert soup is None
  
def test_fetch_html_bbc_top_articles():
    html_file = retrive_test_file_directory("test_bbc.html")
    articles = fetch_bbc_top_articles(html_file)
    assert len(articles) == 5

def test_fetch_html_cnn_top_articles():
  html_file = retrive_test_file_directory("test_cnn.html")
  articles = fetch_cnn_top_articles(html_file)
  assert len(articles) == 5

def test_fetch_html_hacker_news_top_articles():
  html_file = retrive_test_file_directory("test_hacker_rank.html")
  articles = fetch_hacker_news_top_articles(html_file)
  assert len(articles) == 5

def test_fetch_html_business_insider_top_articless():
  html_file = retrive_test_file_directory("business_insider.html")
  articles = fetch_business_insider_top_articles(html_file)
  assert len(articles) == 5

def test_fetch_html_tech_crunch_top_articles():
  html_file = retrive_test_file_directory("tech_crunch.html")
  articles = fetch_tech_crunch_top_articles(html_file)
  assert len(articles) == 5

def test_fetch_html_sky_news_top_articles():
  html_file = retrive_test_file_directory("test_sky_news.html")
  articles = fetch_sky_news_top_articles(html_file)
  assert len(articles) == 5

def test_fetch_html_wired_top_articles():
  html_file = retrive_test_file_directory("test_wired.html")
  articles = fetch_wired_top_articles(html_file)
  assert len(articles) == 5

def test_fetch_html_venture_beat_top_articles():
  html_file = retrive_test_file_directory("test_venture_beat.html")
  articles = fetch_venture_beat_top_articles(html_file)
  assert len(articles) == 5

def test_fetch_html_reddit_top_articles():
  html_file = retrive_test_file_directory("test_reddit.html")
  articles = fetch_reddit_top_articles(html_file, 0)
  assert len(articles) == 5
  
def test_fetch_bbc_top_articles():
    articles = fetch_bbc_top_articles("https://www.bbc.co.uk/news/technology")
    assert len(articles) == 5

def test_fetch_cnn_top_articles():
  articles = fetch_cnn_top_articles("https://edition.cnn.com/business/tech")
  assert len(articles) == 5

def test_fetch_hacker_news_top_articles():
  articles = fetch_hacker_news_top_articles("https://news.ycombinator.com/")
  assert len(articles) == 5

def test_fetch_business_insider_top_articless():
  articles = fetch_business_insider_top_articles("https://www.businessinsider.com/tech")
  assert len(articles) == 5

def test_fetch_tech_crunch_top_articles():
  articles = fetch_tech_crunch_top_articles("https://techcrunch.com/")
  assert len(articles) == 5

def test_fetch_sky_news_top_articles():
  articles = fetch_sky_news_top_articles("https://news.sky.com/technology/")
  assert len(articles) == 5

def test_fetch_wired_top_articles():
  articles = fetch_wired_top_articles("https://www.wired.co.uk/topic/technology/")
  assert len(articles) == 5

def test_fetch_venture_beat_top_articles():
  articles = fetch_venture_beat_top_articles("https://venturebeat.com/")
  assert len(articles) == 5

#Length here to be three not five due to dynamic loading
def test_fetch_reddit_top_articles():
  articles = fetch_reddit_top_articles("https://www.reddit.com/r/technews/", 0)
  assert len(articles) == 3

def test_fetch_reddit_top_articles_offset():
  html_file = retrive_test_file_directory("test_reddit.html")
  articles = fetch_reddit_top_articles(html_file, 2)
  assert len(articles) == 3

def test_fetch_reddit_top_articles_negative_offset():
  html_file = retrive_test_file_directory("test_reddit.html")
  articles = fetch_reddit_top_articles(html_file, -1)
  assert len(articles) == 5
