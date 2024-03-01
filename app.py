from flask import Flask, render_template, url_for
from news_scraper.aggregator import fetch_hacker_news_top_articles, fetch_bbc_top_articles, fetch_cnn_top_articles, fetch_business_insider_top_articles, fetch_tech_crunch_top_articles
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    news_sources = {
        "Hacker News": fetch_hacker_news_top_articles("https://news.ycombinator.com/"),
        "BBC News": fetch_bbc_top_articles("https://www.bbc.co.uk/news/technology"),
        "CNN News": fetch_cnn_top_articles("https://edition.cnn.com/business/tech"),
        "Business Insider": fetch_business_insider_top_articles(
            "https://www.businessinsider.com/tech"
        ),
        "Tech Crunch": fetch_tech_crunch_top_articles("https://techcrunch.com/"),
    }

    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM articles').fetchall()
    conn.close()
    for post in posts:
        print(post[1])

    # return render_template("index.html", news_sources=news_sources)


if __name__ == "__main__":
    app.run(debug=True)