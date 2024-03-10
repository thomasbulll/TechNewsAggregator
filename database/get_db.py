import sys
sys.path.append('../utils/db_utils')
from utils.db_utils import connect_db, retrieve_site_id

def get_articles():
    return {
        "Hacker News": get_articles_by_site_id("Hacker News"),
        "BBC News": get_articles_by_site_id("BBC News"),
        "CNN News": get_articles_by_site_id("CNN News"),
        "Business Insider": get_articles_by_site_id("Business Insider"),
        "Tech Crunch": get_articles_by_site_id("Tech Crunch"),
        "Sky News": get_articles_by_site_id("Sky News"),
        "Wired": get_articles_by_site_id("Wired"),
    }

def get_articles_by_site_id(site):
  site_id = retrieve_site_id(site)
  conn = connect_db()
  cur = conn.cursor()
  query = """
    SELECT a.id, a.article_title, a.article_hash, a.article_url, a.sentiment, s.id AS site_id
    FROM articles AS a
    INNER JOIN sites AS s ON a.site_id = s.id
    WHERE a.site_id = ?
  """
  cur.execute(query, (site_id,))
  articles = cur.fetchall()

  # Convert each row (tuple) to a dictionary
  article_dicts = []
  for row in articles:
    article_dict = {
      "title": row[1],
      "url": row[3],
      "sentiment": row[4],
    }
    article_dicts.append(article_dict)

  return article_dicts

def get_all_hashes():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT article_hash FROM articles")
    results = cur.fetchall()
    hashes = []
    for result in results:
       hashes.append(result[0])
    return hashes

def get_article_by_hash(hash):
  conn = connect_db()
  cur = conn.cursor()
  cur.execute("SELECT * FROM articles WHERE article_hash id = ?", (hash,))
  result = cur.fetchone()
  return {
    "title": result[1],
    "url": result[3],
  }

