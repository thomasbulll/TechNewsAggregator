from .sentiment_analyser import analyze_article
from bs4 import BeautifulSoup
import requests

def extract_bbc_news_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            comments = []
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