import sqlite3
import os
from post_db import init_all_news_sites

current_dir = os.path.dirname(__file__)
schema_file_path = os.path.join(current_dir, 'schema.sql')

connection = sqlite3.connect('database/database.db')

with open(schema_file_path) as f:
    connection.executescript(f.read())

cur = connection.cursor()

init_all_news_sites()

connection.commit()
connection.close()
