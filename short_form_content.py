from database.get_db import get_article_by_hash

def find_new_articles(old_hashes, new_hashes):
    article_hashes =  list(set(new_hashes) - set(old_hashes))
    new_articles = []
    for article_hash in article_hashes:
        new_articles.append(get_article_by_hash(article_hash))
    return new_articles

def generate_short_videos(old_hashes, new_hashes):
    articles = find_new_articles(old_hashes, new_hashes)
