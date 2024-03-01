import sqlite3
import os

current_dir = os.path.dirname(__file__)
schema_file_path = os.path.join(current_dir, 'schema.sql')

connection = sqlite3.connect('database.db')

with open(schema_file_path) as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO sites (title, site_url) VALUES (?, ?)",
            ('Hacker News', 'https://news.ycombinator.com/'))

cur.execute("INSERT INTO sites (title, site_url) VALUES (?, ?)",
            ('BBC', 'https://www.bbc.co.uk/news/technology'))

cur.execute("INSERT INTO articles (site_id, title, title_url, sentiment) VALUES (?, ?, ?, ?)",
            (1, 'TITLE 1', 'title1.com', 0.0))

connection.commit()
connection.close()