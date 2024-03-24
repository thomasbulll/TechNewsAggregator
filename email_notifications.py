from database.email_filters.get_email_filters import get_all_filters
from database.get_db import get_article_by_hash
def send_email(information_array):
    for information in information_array:
        print(information['email'])


def find_new_articles(old_hashes, new_hashes):
    article_hashes =  list(set(new_hashes) - set(old_hashes))
    new_articles = []
    for article_hash in article_hashes:
        new_articles.append(get_article_by_hash(article_hash))
    return new_articles

def emails_needed(old_hashes, new_hashes):

    # Only check the new articles.
    new_articles = find_new_articles(old_hashes, new_hashes)
    if new_articles is None:
        print("emails_needed error: No new articles")
        return
    
    filters = get_all_filters()
    if filters is None:
        print("emails_needed error: No filters")
        return
    
    find_correct_recipients(new_articles, filters)

def find_correct_recipients(articles, filters):
    """
    Retrives any possible article that the user would like to filter
    based on an email filte that they have supplied.

    Args:
        articles: A list of dictionaries, with url and title as the keys.
        filters: A dictionary, with the keyword as the key and a list of users as the value

    Returns:
        A list of dictionaries, with the users email, article title and url as the keys.
        The dictionaries represent each email that needs to  be sent.
    """
    pending_emails = []

    # n - The number of articles
    # k - The number of filters
    # j - The number of words in an article's title
    # Time complexity - O(n*k*j)

    for article in articles:
        title = article['title'].lower()
        words = title.split()
        # Loop through the title to check if the word is within
        for word in words:
            word_lower = word.lower()
            if filters.get(word_lower) is not None:
                # Loop through all the users that have that filter
                for email in filters.get(word_lower):
                    notification = {'title': title, 'url':article['url'], 'email':email, 'word':word}
                    pending_emails.append(notification)

    return pending_emails
