import sqlite3
import hashlib
import os

def post_all_articles(news_sources):
    for source_name, articles in news_sources.items():
        for article in articles:
            post_news_article(article['title'], article['url'], article['sentiment'], source_name)

def connect_db():
    connection = sqlite3.connect('database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

# One time use, only use when the data needs to be reset.
def init_all_news_sites():
    sites = [
    {"title": "BBC News", "url": "https://www.bbc.co.uk/news/technology"},
    {"title": "Hacker News", "url": "https://news.ycombinator.com/"},
    {"title": "CNN News", "url": "https://edition.cnn.com/business/tech"},
    {"title": "Business Insider", "url": "https://www.businessinsider.com/tech"},
    {"title": "Tech Crunch", "url": "https://techcrunch.com/"},
    ]

    for site in sites:
        if "title" in site and "url" in site:
            post_news_source(site['title'], site['url'])
        else:
            print("init_all_news_sites error: could not add sites to db ")
    
def post_news_article(title, url, sentiment, site_title):
    conn = connect_db()

    try:
        cur = conn.cursor()

        sentiment_title = ''

        if sentiment > 0.05:
            sentiment_title = "positive"
        elif sentiment < -0.05:
            sentiment_title = "negative"
        else:
            sentiment_title = "neutral"

        site_id = retrieve_site_id(site_title)
        if site_id:
            cur.execute("INSERT INTO articles (article_title, article_hash, article_url,sentiment, site_id) VALUES (?, ?, ?, ?, ?)",
                (title, get_hash(title), url, sentiment_title, site_id))
            conn.commit()
        else:
            print("post_news_article error: unable to retrieve site_id")

    finally:
        conn.close()

def retrieve_site_id(site_title):
    conn = connect_db()

    try:
        cur = conn.cursor()

        cur.execute("SELECT id FROM sites WHERE site_title = ?", (site_title,))
        conn.commit()
        site_data = cur.fetchone()

        if not site_data:
            print("retrieve_site_id error: no matching site found")
            return None

        return site_data['id']

    finally:
        conn.close()

def get_hash(title):
    hash_object = hashlib.sha256(title.encode('utf-8'))
    hex_digest = hash_object.hexdigest()

    hash_bytes = bytes.fromhex(hex_digest)

    return hash_bytes

def post_news_source(title, url):
    conn = connect_db()

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO sites (site_title, site_url) VALUES (?, ?)", (title, url))
        conn.commit()

    finally:
        conn.close()
    