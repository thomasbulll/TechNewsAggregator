import requests
from bs4 import BeautifulSoup

def getCNNResults():
    url = "https://edition.cnn.com/business/tech"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")
            cnn_articles = []
            articles = soup.find_all("a", class_="container__link")
            i = 0
            urlSet = set()
            while len(cnn_articles) <= 4:
                titleTag = articles[i].find("span", class_="container__headline-text")
                if titleTag:
                    wordTitle = titleTag.text
                    titleUrl = "https://edition.cnn.com" + articles[i]["href"]
                    if titleUrl not in urlSet:
                        urlSet.add(titleUrl)
                        article = {'title': wordTitle, 'url': titleUrl}
                        cnn_articles.append(article)
                i += 1
            return cnn_articles
        else:
            print(f"Failed to fetch content from {url}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CNN content: {e}")
        return []
    
def getBbcNewsResutls():
    url = "https://www.bbc.co.uk/news/technology"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            soup = BeautifulSoup(page_content, "html.parser")
            bbc_news_articles = []
            articles = []
            all_a_tags = soup.find_all("a")

            #  Extract "PromoLink" anchor tags with adaptive class name filtering since
            #  class names change dynamically, we'll loop through all anchor tags check
            #  if the href is a link to an article.
            for tag in all_a_tags:
                itemLink = tag["href"]
                if itemLink[:17] == "/news/technology-":
                    articles.append(tag)
            
            for i in range(0, 5):
                spanChildren = articles[i].findChildren("span")
                for c in range(0, len(spanChildren)):
                    if c % 2 == 0 and spanChildren[c].text != None:
                        titleTag = articles[i]
                        titleUrl = titleTag["href"]
                        wordTitle = spanChildren[c].text
                        # Create a dictionary for each article
                        article = {'title': wordTitle, 'url': titleUrl}
                        bbc_news_articles.append(article)
            return bbc_news_articles
        else:
            print(f"Failed to fetch content from {url}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching BBC content: {e}")
        return []
    
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
            for i in range(0, 5):
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
        print(f"Error fetching Hacker Rank content: {e}")
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
        else:
            print(f"Failed to fetch content from {url}")
            return
    except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return