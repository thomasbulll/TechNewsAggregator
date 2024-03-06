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

# If a user manually wants to delete a filter
def delete_specific_email_filter_by_id(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM email_filters WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# If a user deletes their account
def delete_specific_email_filter_by_user_email(email):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM email_filters WHERE email = ?", (email,))
    conn.commit()
    conn.close()