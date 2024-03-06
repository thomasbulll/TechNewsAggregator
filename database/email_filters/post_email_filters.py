import sys
sys.path.append('../../utils/db_utils')
from utils.db_utils import connect_db
from database.email_filters.get_email_filters import get_all_ids_per_user

def insert_new_email_filter(key_word, email):
    conn = connect_db()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO email_filters (key_word, email) VALUES (?, ?)", (key_word, email))
        conn.commit()

    finally:
        conn.close()

# If a user manually wants to delete a filter
def delete_specific_email_filter_by_id(id, email):
    print("delete_specific_email_filter_by_id")
    conn = connect_db()
    cur = conn.cursor()
    filters = get_all_ids_per_user(email)
    found = False
    for filter in filters:
        if filter == id:
            found = True
    if found:
        cur.execute("DELETE FROM email_filters WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

# If a user deletes their account
def delete_specific_email_filter_by_user_email(email):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM email_filters WHERE email = ?", (email,))
    conn.commit()
    conn.close()