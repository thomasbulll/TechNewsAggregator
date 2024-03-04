import sys
sys.path.append('../utils/db_utils')
from utils.db_utils import connect_db, retrieve_site_id
from models import User

def get_articles():
    return {
        "Hacker News": get_articles_by_site_id("Hacker News"),
        "BBC News": get_articles_by_site_id("BBC News"),
        "CNN News": get_articles_by_site_id("CNN News"),
        "Business Insider": get_articles_by_site_id("Business Insider"),
        "Tech Crunch": get_articles_by_site_id("Tech Crunch"),
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

def check_username_exists(username):
  if username is None or len(username) < 1:
     return False
  conn = connect_db()
  cur = conn.cursor()
  cur.execute("SELECT * FROM users WHERE username = ?", (username,))
  result = cur.fetchall()
  if result:
     return result
  return None

def check_email_exists(email):
  if email is None or len(email) < 1:
     return False
  conn = connect_db()
  cur = conn.cursor()
  cur.execute("SELECT * FROM users WHERE email = ?", (email,))
  result = cur.fetchall()
  if result:
     return result
  return None

def check_login_username(username):
  conn = connect_db()
  cur = conn.cursor()
  cur.execute("SELECT * FROM users WHERE username = ?", (username,))
  result = cur.fetchone()
  if result:
        is_active = True
        return User(result[0], result[1], result[2], is_active)
  return None

def check_password(username, password_hash):
  conn = connect_db()
  cur = conn.cursor()
  cur.execute("SELECT username FROM users WHERE password_hash = ?", (password_hash,))
  result = cur.fetchone()
  if result and result[0] == username:
     return True
  return False

def get_user_from_id(id):
  conn = connect_db()
  cur = conn.cursor()
  cur.execute("SELECT * FROM users WHERE id = ?", (id,))
  result = cur.fetchone()
  if result:
     return result
  return None