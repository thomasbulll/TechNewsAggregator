from .sentiment_analyser import analyze_article
from bs4 import BeautifulSoup
import requests

def extract_bbc_news_article_sentiment(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")
            article = soup.find(id="main-content")
            return analyze_article(article.text)
        else:
            print(f"Failed to fetch content from {url}")
            return
    except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return
    
def extract_cnn_news_article_sentiment(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")
            article = soup.find(class_="article__main")
            return analyze_article(article.text)
        else:
            print(f"Failed to fetch content from {url}")
            return
    except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return
    
def extract_tech_crunch_article_sentiment(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")
            article = soup.find(class_="article-content")
            return analyze_article(article.text)
        else:
            print(f"Failed to fetch content from {url}")
            return
    except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return

def extract_sky_news_article_sentiment(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")
            article = soup.find(class_="sdc-article-body")
            return analyze_article(article.text)
        else:
            print(f"Failed to fetch content from {url}")
            return
    except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return
    
def extract_wired_article_sentiment(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")
            article = soup.find(class_="body__inner-container")
            print(article.text)
            return analyze_article(article.text)
        else:
            print(f"Failed to fetch content from {url}")
            return
    except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return
    