import sys
sys.path.append('../../utils/db_utils')
from utils.db_utils import connect_db

def insert_new_email_filter(key_word, email):
    conn = connect_db()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO email_filters (key_word, email) VALUES (?, ?)", (key_word, email))
        conn.commit()

    finally:
        conn.close()
