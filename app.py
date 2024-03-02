from flask import Flask, render_template, url_for
from news_scraper.aggregator import fetch_hacker_news_top_articles, fetch_bbc_top_articles, fetch_cnn_top_articles, fetch_business_insider_top_articles, fetch_tech_crunch_top_articles
import sqlite3
from database.get_db import get_articles

app = Flask(__name__)

@app.route("/")
def index():
    news_sources = get_articles()
    return render_template("index.html", news_sources=news_sources)

if __name__ == "__main__":
    app.run(debug=True)
