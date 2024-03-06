from database.get_db import get_article_by_hash
from bs4 import BeautifulSoup
import requests

def find_all_text_in_body(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            soup =  BeautifulSoup(page_content, "html.parser")
            body = soup.find("body")
            return body.text
        else:
            print(f"Failed to fetch content from {url}")
            return
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return

def find_new_articles(old_hashes, new_hashes):
    article_hashes =  list(set(new_hashes) - set(old_hashes))
    new_articles = []
    for article_hash in article_hashes:
        new_articles.append(get_article_by_hash(article_hash))
    return new_articles

def generate_short_videos(old_hashes, new_hashes):
    articles = find_new_articles(old_hashes, new_hashes)
