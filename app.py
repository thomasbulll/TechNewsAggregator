from flask import Flask, render_template
from news_scraper.aggregator import fetch_hacker_news_top_articles, fetch_bbc_top_articles, fetch_cnn_top_articles, fetch_business_insider_top_articles, fetch_tech_crunch_top_articles

app = Flask(__name__)

@app.route('/')
def index():
    hacker_news_articles = fetch_hacker_news_top_articles("https://news.ycombinator.com/")
    bbc_news_articles = fetch_bbc_top_articles("https://www.bbc.co.uk/news/technology")
    cnn_news_articles = fetch_cnn_top_articles("https://edition.cnn.com/business/tech")
    business_insider_articles = fetch_business_insider_top_articles("https://www.businessinsider.com/tech")
    tech_crunch_articles = fetch_tech_crunch_top_articles("https://techcrunch.com/")
    # the_next_web_articles = fetch_the_next_web_top_articles("https://thenextweb.com/")

    return render_template('index.html', hacker_news_articles=hacker_news_articles, 
                           bbc_news_articles=bbc_news_articles, 
                           cnn_news_articles=cnn_news_articles, 
                           business_insider_articles=business_insider_articles,
                           tech_crunch_articles=tech_crunch_articles)
        
if __name__ == "__main__":
    # fetch_the_next_web_top_articles("https://thenextweb.com/")
    app.run(debug=True)