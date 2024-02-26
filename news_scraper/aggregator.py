import requests
from bs4 import BeautifulSoup
from typing import Optional

def fetch_parsed_html(url):
    try:
        if url[:5] == "https":
            response = requests.get(url)
            if response.status_code == 200:
                page_content = response.text
                soup =  BeautifulSoup(page_content, "html.parser")
                return soup
            else:
                print(f"Failed to fetch content from {url}")
                return
        else:
            fetch_local_parsed_html(url)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return
    
def fetch_local_parsed_html(url):
    try:
        with open(url, "r") as f:
            html_content = f.read()
        return BeautifulSoup(html_content, features="html.parser")
    except IOError as e:
        print(f"Error fetching content: {e}")
        return

def trim_title(title):
    max_length = 125
    truncated_text = title[:max_length - 3]
    return f"{truncated_text}..."
    
def fetch_business_insider_top_articles(url):
    soup = fetch_parsed_html(url)
    business_insider_articles = []
    articles = soup.find_all("a", class_="tout-title-link")
    for i in range(0, 5):
        article = articles[i]
        article_title = article.text
        title_url = "https://www.businessinsider.com" + article["href"]
        if len(article_title) > 120:
            article_title = trim_title(article_title)
        business_article = {'title': article_title, 'url': title_url}
        business_insider_articles.append(business_article)
    return business_insider_articles

def fetch_tech_crunch_top_articles(url):
    soup = fetch_parsed_html(url)
    tech_crunch_articles = []
    articles = soup.find_all("a", class_="post-block__title__link")
    unique_article_urls = set()
    i = 0
    while len(tech_crunch_articles) <= 4:
        article = articles[i]
        article_title = article.text
        title_url = article["href"]
        if len(article_title.strip()) > 0 and title_url not in unique_article_urls:
            unique_article_urls.add(title_url)
            if len(article_title) > 120:
                article_title = trim_title(article_title)
            tc_article = {'title': article_title, 'url': title_url}
            tech_crunch_articles.append(tc_article)
        i += 1
    return tech_crunch_articles

def fetch_cnn_top_articles(url):
    soup = fetch_parsed_html(url)
    cnn_articles = []
    articles = soup.find_all("a", class_="container__link")
    i = 0
    unique_article_urls = set()
    while len(cnn_articles) <= 4:
        title_tag = articles[i].find("span", class_="container__headline-text")
        if title_tag:
            article_title = title_tag.text
            article_url = "https://edition.cnn.com" + articles[i]["href"]
            # Removes articles from other topics as they are also displayed on tech page
            if articles[i]["href"][12:16] == "tech" and article_url not in unique_article_urls:
                if len(article_title) > 120:
                    article_title = trim_title(article_title)
                unique_article_urls.add(article_url)
                article = {'title': article_title, 'url': article_url}
                cnn_articles.append(article)
        i += 1
    return cnn_articles

def fetch_bbc_top_articles(url):
    soup = fetch_parsed_html(url)
    bbc_news_articles = []
    article_tags = []
    all_a_tags = soup.find_all("a")

    # Extract "PromoLink" anchor tags with adaptive class name filtering since
    # class names change dynamically, we'll loop through all anchor tags check
    # if the href is a link to an article.
    for tag in all_a_tags:
        item_link = tag["href"]
        if item_link[:17] == "/news/technology-":
            article_tags.append(tag)

    for i in range(5):  # Fetch only 5 articles
        article_elements = article_tags[i].findChildren("span")
        for c in range(len(article_elements)):
            if c % 2 == 0 and article_elements[c].text is not None:
                title_tag = article_tags[i]
                title_url = "https://www.bbc.co.uk" + title_tag["href"]
                article_title = article_elements[c].text
                # Create a dictionary for each article
                if len(article_title) > 120:
                    article_title = trim_title(article_title)
                article = {'title': article_title, 'url': title_url}
                bbc_news_articles.append(article)
    return bbc_news_articles

def fetch_hacker_news_top_articles(url):
    soup = fetch_parsed_html(url)
    articles = soup.find_all("tr", class_="athing")
    # subline = soup.find_all("span", class_="subline")
    hacker_news_articles = []
    for i in range(5):
        title_link = articles[i].find("span", class_="titleline")
        if title_link:
            title = title_link.find("a")
            if title:
                article_title = title.text
                article_url = title["href"]
                if len(article_title) > 120:
                    article_title = trim_title(article_title)
                article_data = {"title": article_title, "url": article_url}
                hacker_news_articles.append(article_data)
        else:
            print("Title nor link not found")

            # Extract comments
            # if subline:
            #     get_hacker_news_subline(url, subline)
            # else:
            #     print("Subline not found")

    return hacker_news_articles  # Return values directly

def get_hacker_news_subline(url, subline):
    subline_content = subline.findChildren("a")
    for item in subline_content:
        item_link = item["href"]
        if item_link.startswith("item"):
            fetch_hacker_news_comments(url + item_link)

def fetch_hacker_news_comments(url):
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
    