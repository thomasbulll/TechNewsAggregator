from database.email_filters.get_email_filters import get_all_filters
from database.get_db import get_articles_by_site_id

#Terrible temporary solution
def check_all_filters():
    filters = get_all_filters()
    pending_emails = []
    all_filters = {}
    
    # Put all the email filters in a hashmap, with the key being the filter
    # and the value being the list of user emails where they want to filter that key.
    for filter in filters:
        all_filters[filter.key_word.lower()] = all_filters.get(filter.key_word.lower(), []).append(filter.email)

    # Loop through the different news site's articles e.g. BBC News, CNN etc...
    for articles in get_all_articles():
        # Loop through the articles from that single source
        for article in articles:
            title = article.title
            words = title.split()
            # Loop through the title to check if the word is within
            for word in words:
                if all_filters[word]:
                    # Loop through all the users that have that filter
                    for email in all_filters.get():
                        notification = {'title': article.title, 'url':article.url, 'email':email}
                        pending_emails.append(notification)
    for filter in pending_emails:
        print(filter.title)
        print(filter.email)
        
def get_all_articles():
    return [get_articles_by_site_id("Hacker News"), get_articles_by_site_id("BBC News"),
            get_articles_by_site_id("CNN News"), get_articles_by_site_id("Business Insider"),
            get_articles_by_site_id("Tech Crunch"), get_articles_by_site_id("Sky News"),
            get_articles_by_site_id("Wired"), get_articles_by_site_id("Venture Beat")]
