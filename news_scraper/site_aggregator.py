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
    
def extract_business_insider_article_sentiment(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")
            paragraphs = soup.find_all("p", class_="premium")
            text = ""
            for paragraph in paragraphs:
                 if paragraph:
                    text += paragraph.text
            return analyze_article(text)
        else:
            print(f"Failed to fetch content from {url}")
            return
    except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return

def extract_reddit_article_sentiment(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")
            posts = soup.find_all("shreddit-post")
            return analyze_article(posts[0].text)
        else:
            print(f"Failed to fetch content from {url}")
            return
    except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return
    
def extract_generic_article_sentiment(url, className):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")
            article = soup.find(class_=className)
            return analyze_article(article.text)
        else:
            print(f"Failed to fetch content from {url}")
            return
    except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return
            