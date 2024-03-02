import sqlite3
import os
from post_db import post_news_source, post_news_article

current_dir = os.path.dirname(__file__)
schema_file_path = os.path.join(current_dir, 'schema.sql')

connection = sqlite3.connect('database/database.db')

with open(schema_file_path) as f:
    connection.executescript(f.read())

cur = connection.cursor()

# post_news_source('BBC News', 'https://www.bbc.co.uk/news/technology')

# post_news_source('Hacker News', 'https://news.ycombinator.com/')

# post_news_article('TITLE 1', 'title1.com', 0.1, 'BBC News')

# post_news_article('TITLE 2', 'title1.com', 0.1, 'BBC News')

# post_news_article('TITLE 3', 'title1.com', 0.1, 'BBC News')

connection.commit()
connection.close()