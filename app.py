import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

# def getBbcNewsResutls():
#     url = "https://www.bbc.co.uk/news/technology"
#     response = requests.get(url)
#     if response.status_code == 200:
#         page_content = response.text
#         soup = BeautifulSoup(page_content, "html.parser")
#         articles = soup.find_all("li", class_="ListItem")
#         for article in articles:
#             link = article.find("a", class_="PromoLink")["href"]
#             extractBbcNewsComments(link)
            
# def extractBbcNewsComments(url):
#     url = "https://www.bbc.co.uk" + url
#     print("BBC: \n{url}\n")
    
def getHackerNewsResults():
    url = "https://news.ycombinator.com/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")
            articles = soup.find_all("tr", class_="athing")
            # subline = soup.find_all("span", class_="subline")
            # Create a list to store articles (dictionaries)
            hacker_news_articles = []
            for i in range(0, 10):
                # Extract title and url
                titlelink = articles[i].find("span", class_="titleline")
                if titlelink:
                    title = titlelink.find("a")
                    if title:
                        wordTitle = title.text
                        titleUrl = title["href"]

                        # Create a dictionary for each article
                        article = {'title': wordTitle, 'url': titleUrl}
                        hacker_news_articles.append(article)
                else:
                    print("Title nor link not found")

                    # Extract comments
                    # if subline:
                    #     sublineContent = subline[i].findChildren("a")
                    #     for item in sublineContent:
                    #         itemLink = item["href"]
                    #         if itemLink[:4] == "item":
                    #             getHackerNewsComment(url + itemLink)
                    # else:
                    #     print("Subline not found")

            # Return the list of articles
            return hacker_news_articles

        else:
            print(f"Failed to fetch content from {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return []  # Return an empty list in case of errors

    return []  # Return an empty list if no data is found

def getHackerNewsComment(url):
    print(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            comments = []
            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")
            articles = soup.find_all("span", class_="commtext c00")
            for i in range(0, len(articles)):
                comment = ""
                body = articles[i].findChildren()
                if body:
                    for segment in body:
                        comment = comment + " " + segment.text
                comments.append(comment)
        return comments
    except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return
    
def main():
    getHackerNewsResults()

@app.route('/')
def index():
    hacker_news_articles = getHackerNewsResults()

    return render_template('index.html', hacker_news_articles=hacker_news_articles)
        
if __name__ == "__main__":
    app.run(debug=True)