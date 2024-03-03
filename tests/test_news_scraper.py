import sys
sys.path.append("..")
from news_scraper.aggregator import fetch_hacker_news_top_articles, fetch_bbc_top_articles, fetch_cnn_top_articles, fetch_parsed_html
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

# Pass in complete path and uncomment tests to verify this behaviour
  
def test_fetch_bbc_top_articles():
    html_file = retrive_test_file_directory("test_bbc.html")
    articles = fetch_bbc_top_articles(html_file)
    assert articles != None

def test_fetch_cnn_top_articles():
  html_file = retrive_test_file_directory("test_cnn.html")
  articles = fetch_cnn_top_articles(html_file)
  assert articles != None

def test_fetch_hacker_news_top_articles():
  html_file = retrive_test_file_directory("test_hacker_rank.html")
  articles = fetch_hacker_news_top_articles(html_file)
  assert articles != None
