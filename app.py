from flask import Flask, render_template
from news_scraper.aggregator import getHackerNewsResults, getBbcNewsResutls

app = Flask(__name__)

@app.route('/')
def index():
    hacker_news_articles = getHackerNewsResults()
    bbc_news_articles = getBbcNewsResutls()

    return render_template('index.html', hacker_news_articles=hacker_news_articles, bbc_news_articles=bbc_news_articles)
        
if __name__ == "__main__":
    app.run(debug=True)