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
    
def delete_specific_user_by_id(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()