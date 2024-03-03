from news_scraper.aggregator import fetch_hacker_news_top_articles, fetch_bbc_top_articles, fetch_cnn_top_articles, fetch_business_insider_top_articles, fetch_tech_crunch_top_articles
from database.post_db import post_all_articles, reset_artice_table
from apscheduler.schedulers.background import BackgroundScheduler
from database.get_db import get_articles
from flask import Flask, render_template

app = Flask(__name__)

def get_all_articles():
    return {
        "Hacker News": fetch_hacker_news_top_articles("https://news.ycombinator.com/"),
        "BBC News": fetch_bbc_top_articles("https://www.bbc.co.uk/news/technology"),
        "CNN News": fetch_cnn_top_articles("https://edition.cnn.com/business/tech"),
        "Business Insider": fetch_business_insider_top_articles(
            "https://www.businessinsider.com/tech"
        ),
        "Tech Crunch": fetch_tech_crunch_top_articles("https://techcrunch.com/"),
    }

# Temporary solution, delete all the contents of the articles table
# and fill it with the new articles once an hour.
def get_new_articles():
    print("GET NEW ARTICLES")
    reset_artice_table()
    post_all_articles(get_all_articles())

scheduler = BackgroundScheduler()
scheduler.add_job(get_new_articles, 'interval', hours=1)
scheduler.start()

@app.route("/")
def index():
    news_sources = get_articles()
    return render_template("index.html", news_sources=news_sources)

if __name__ == "__main__":
    app.run(debug=True)
