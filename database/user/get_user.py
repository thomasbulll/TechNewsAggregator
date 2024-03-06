import sys
sys.path.append('../utils/db_utils')
from utils.db_utils import connect_db
from models import User

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
      is_active = True
      return User(result[0], result[1], result[2], is_active)
  return None