import sys
sys.path.append('../../utils/db_utils')
from utils.db_utils import connect_db

def post_new_user(username, email, password_hash):
    conn = connect_db()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash))
        conn.commit()

    finally:
        conn.close()