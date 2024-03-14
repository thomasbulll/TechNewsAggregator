from .sentiment_analyser import analyze_reviews
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os

def get_hacker_news_subline(url, subline):
    """
    Extracts the link to the comments from the html, then calls fetch_hacker_news_comments which
    returns the list of comments

    Args:
        subline: Takes in a html element "subline" which will contain the link to visit the comments.
        url: need to append the subline comment link to the main url to get a functioning url

    Returns:
        A sentiment avg
    """
    subline_content = subline.findChildren("a")
    for item in subline_content:
        item_link = item["href"]
        if item_link.startswith("item"):
            return fetch_hacker_news_comments(url + item_link)

def fetch_hacker_news_comments(url):
    """
    Extracts comments from the html, sends them through the sentiment analysis method to find the avg.

    Args:
        url: the url to access the comments for a specific article

    Returns:
        A sentiment avg
    """
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
            return analyze_reviews(comments)
        else:
            print(f"Failed to fetch content from {url}")
            return
    except requests.exceptions.RequestException as e:
            print(f"Error fetching content: {e}")
            return
    
# Currently can't access the comments
def check_if_bbc_contans_comments(url):
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text
        soup =  BeautifulSoup(page_content, "html.parser")
        all_spans = soup.find_all("button")
        for span in all_spans:
            if span.text == "View comments":
                return get_all_bbc_news_comments(span['class'], url)
    return None

def get_all_bbc_news_comments(class_name, url):
    driver = webdriver.Chrome(os.environ.get('CHROME_DRIVER')) 
    driver.get(url)
    button = driver.find_element(By.CLASS_NAME, class_name)
    button.click()
    updated_html = driver.page_source
    soup = BeautifulSoup(updated_html, "html.parser")
    all_div = soup.find_all("div")
    bbc_comments = []
    for div in all_div:
        if div['class'][14:28] == "CommentBubble":
            bbc_comments.append(div.text)
    return analyze_reviews(bbc_comments)
