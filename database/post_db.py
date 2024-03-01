import sqlite3
import hashlib
import os

# def post_all_articles(news_sources):

#     cur = connection.cursor()

#     for source_name, articles in news_sources.items():
#         for article in articles:
#             print(f"\tTitle: {article['title']}")
#             print(f"\tURL: {article['url']}")
#             print(f"\tSentiment: {article['sentiment']}")
#         source_id_map = {}
#         for source_name in news_sources.keys():
#             source_id = hashlib.sha256(source_name.encode('utf-8')).hexdigest()
#             source_id_map[source_name] = source_id
    
def post_news_article(title, url, sentiment, site_title):
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row

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
        else:
            print("post_news_article error: unable to retrieve site_id")

    finally:
        conn.close()

def retrieve_site_id(site_title):
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row

    try:
        cur = conn.cursor()

        cur.execute("SELECT id FROM sites WHERE site_title = ?", (site_title,))

        site_data = cur.fetchall()

        print(str(len(site_data)))

        if site_data is not None:
            return site_data
        else:
            print("retrieve_site_id error: site_data queried none")
            return None
    finally:
        conn.close()

def get_hash(title):
    hash_object = hashlib.sha256(title.encode('utf-8'))
    hex_digest = hash_object.hexdigest()

    hash_bytes = bytes.fromhex(hex_digest)

    return hash_bytes

def post_news_source(title, url):
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row

    try:
        cur = conn.cursor()

        cur.execute("INSERT INTO sites (site_title, site_url) VALUES (?, ?)",
                (title, url))
        
        cur.execute("SELECT * FROM sites")
        sites = cur.fetchall()
        print(str(len(sites)))

    finally:
        conn.close()
    