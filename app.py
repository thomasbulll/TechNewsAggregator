from flask import Flask, render_template
from news_scraper.aggregator import fetch_hacker_news_top_articles, fetch_bbc_top_articles, fetch_cnn_top_articles

app = Flask(__name__)

@app.route('/')
def index():
    hacker_news_articles = fetch_hacker_news_top_articles()
    bbc_news_articles = fetch_bbc_top_articles()
    cnn_news_articles = fetch_cnn_top_articles()

    return render_template('index.html', hacker_news_articles=hacker_news_articles, bbc_news_articles=bbc_news_articles, cnn_news_articles=cnn_news_articles)
        
if __name__ == "__main__":
    app.run(debug=True)