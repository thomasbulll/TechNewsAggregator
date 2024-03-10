import requests
from bs4 import BeautifulSoup
from .comment_aggregator import get_hacker_news_subline

def fetch_parsed_html(url):
    """
    Fetches the beautiful soup of a website's url, if the url 
    belongs to a file url, it will automatically call the 
    method fetch_local_parsed_html to handle it.

    Args:
        url: The url of the website / local file we want to scrape

    Returns:
        The beautiful soup of the given website url
    """
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
            return fetch_local_parsed_html(url)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return
    
def fetch_local_parsed_html(url):
    """
    Fetches the beautiful soup of local html file

    Args:
        url: Local html file url

    Returns:
        The beautiful soup of a given html file
    """
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
    """
    Fetches the top 5 articles from Business Insider

    Args:
        url: The URL of the Business Insider website.

    Returns:
        A list of dictionaries, where each dictionary represents an article with the
        following keys:
            - title: The title of the article.
            - url: The URL of the article.
            - sentiment: The sentiment analysis of the comments (if available).
    """

    soup = fetch_parsed_html(url)
    business_insider_articles = []
    articles = soup.find_all("a", class_="tout-title-link")
    for i in range(0, 5):
        article = articles[i]
        article_title = article.text
        title_url = "https://www.businessinsider.com" + article["href"]
        if len(article_title) > 120:
            article_title = trim_title(article_title)
        business_article = {'title': article_title, 'url': title_url, "sentiment": 0.0}
        business_insider_articles.append(business_article)
    return business_insider_articles

def fetch_tech_crunch_top_articles(url):
    """
    Fetches the top 5 articles from Tech Crunch

    Args:
        url: The URL of the Tech Crunch website.

    Returns:
        A list of dictionaries, where each dictionary represents an article with the
        following keys:
            - title: The title of the article.
            - url: The URL of the article.
            - sentiment: The sentiment analysis of the comments (if available).
    """

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
            tc_article = {'title': article_title, 'url': title_url, "sentiment": 0.0}
            tech_crunch_articles.append(tc_article)
        i += 1
    return tech_crunch_articles

def fetch_cnn_top_articles(url):
    """
    Fetches the top 5 articles from CNN

    Args:
        url: The URL of the CNN News website.

    Returns:
        A list of dictionaries, where each dictionary represents an article with the
        following keys:
            - title: The title of the article.
            - url: The URL of the article.
            - sentiment: The sentiment analysis of the comments (if available).
    """

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
                article = {'title': article_title, 'url': article_url, "sentiment": 0.0}
                cnn_articles.append(article)
        i += 1
    return cnn_articles

def fetch_bbc_top_articles(url):
    """
    Fetches the top 5 articles from the BBC

    Args:
        url: The URL of the BBC News website.

    Returns:
        A list of dictionaries, where each dictionary represents an article with the
        following keys:
            - title: The title of the article.
            - url: The URL of the article.
            - sentiment: The sentiment analysis of the comments (if available).
    """

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
                article = {'title': article_title, 'url': title_url, "sentiment": 0.0}
                bbc_news_articles.append(article)
    return bbc_news_articles

def fetch_hacker_news_top_articles(url):
    """
    Fetches the top 5 articles from Hacker News

    Args:
        url: The URL of the Hacker News website.

    Returns:
        A list of dictionaries, where each dictionary represents an article with the
        following keys:
            - title: The title of the article.
            - url: The URL of the article.
            - sentiment: The sentiment analysis of the comments (if available).
    """

    soup = fetch_parsed_html(url)
    articles = soup.find_all("tr", class_="athing")
    subline = soup.find_all("span", class_="subline")
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
                # Extract comments
                if subline:
                    comment_sentiment = get_hacker_news_subline(url, subline[i])
                article_data = {"title": article_title, "url": article_url, "sentiment": comment_sentiment}
                hacker_news_articles.append(article_data)
        else:
            print("Title nor link not found")

    return hacker_news_articles  # Return values directly

def fetch_sky_news_top_articles(url):
    """
    Fetches the top 5 articles from Sky News

    Args:
        url: The URL of the Sky News website.

    Returns:
        A list of dictionaries, where each dictionary represents an article with the
        following keys:
            - title: The title of the article.
            - url: The URL of the article.
            - sentiment: The sentiment analysis of the comments (if available).
    """

    soup = fetch_parsed_html(url)
    articles = soup.find_all("div", class_="grid-cell")
    sky_news_articles = []
    for i in range(5):
        title_link = articles[i].find("a")
        if title_link:
            article_title = title_link.text
            article_url = "https://news.sky.com/technology/" + title_link["href"]
            if len(article_title) > 120:
                article_title = trim_title(article_title)
            article_data = {"title": article_title, "url": article_url, "sentiment": 0.0}
            sky_news_articles.append(article_data)
        else:
            print("Title nor link not found")

    return sky_news_articles  # Return values directly

def fetch_wired_top_articles(url):
    """
    Fetches the top 5 articles from Wired

    Args:
        url: The URL of the Wired website.

    Returns:
        A list of dictionaries, where each dictionary represents an article with the
        following keys:
            - title: The title of the article.
            - url: The URL of the article.
            - sentiment: The sentiment analysis of the comments (if available).
    """

    soup = fetch_parsed_html(url)
    articles = soup.find_all("div", class_="summary-item__content")
    wired_articles = []
    # Start at index 1 to avoid adverts
    for i in range(1, 6):
        title_link = articles[i].find("a")
        if title_link:
            article_title = title_link.text
            article_url = "https://www.wired.co.uk/topic/technology/" + title_link["href"]
            if len(article_title) > 120:
                article_title = trim_title(article_title)
            article_data = {"title": article_title, "url": article_url, "sentiment": 0.0}
            wired_articles.append(article_data)
        else:
            print("Title nor link not found")

    return wired_articles  # Return values directly