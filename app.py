from flask import Flask, render_template
from NewsScraping.scraper import getHackerNewsResults

app = Flask(__name__)

@app.route('/')
def index():
    hacker_news_articles = getHackerNewsResults()

    return render_template('index.html', hacker_news_articles=hacker_news_articles)
        
if __name__ == "__main__":
    app.run(debug=True)