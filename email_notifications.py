from database.email_filters.get_email_filters import get_all_filters
from database.get_db import get_articles_by_site_id, get_article_by_hash

def find_new_articles(old_hashes, new_hashes):
    article_hashes =  list(set(new_hashes) - set(old_hashes))
    new_articles = []
    for article_hash in article_hashes:
        new_articles.append(get_article_by_hash(article_hash))
    return new_articles

# Terrible temporary solution
def check_all_filters(old_hashes, new_hashes):

    # Only check the new articles.
    new_articles = find_new_articles(old_hashes, new_hashes)
    if new_articles is None:
        print("check_all_filters error: No new articles")
        return
    
    filters = get_all_filters()
    if filters is None:
        print("check_all_filters error: No filters")
        return
    
    all_filters = {}
    
    # Put all the email filters in a hashmap, with the key being the filter
    # and the value being the list of user emails where they want to filter that key.
    for filter in filters:
        all_filters[filter['key_word'].lower()] = all_filters.get(filter['key_word'].lower(), []).append(filter['email'])
    
    find_correct_recipients(new_articles, all_filters)


def find_correct_recipients(articles, filters):
    pending_emails = []

    # Loop through the new articles
    for article in articles:
        title = article['title']
        words = title.split()
        # Loop through the title to check if the word is within
        for word in words:
            if filters.get(word) is not None:
                # Loop through all the users that have that filter
                for email in filters.get(word):
                    notification = {'title': article['title'], 'url':article['url'], 'email':email}
                    pending_emails.append(notification)

    return pending_emails