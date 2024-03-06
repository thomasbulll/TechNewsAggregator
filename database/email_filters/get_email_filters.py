import sys
sys.path.append('../../utils/db_utils')
from utils.db_utils import connect_db

def get_all_ids_per_user(email):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM email_filters WHERE email = ?", (email,))
    results = cur.fetchall()
    if results is None:
        return None
    ids = []
    for result in results:
        ids.append(result[0])
    return ids

def get_all_filters_per_user(email):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM email_filters WHERE email = ?", (email,))
    results = cur.fetchall()
    if results is None:
        return None
    filters = []
    for result in results:
        filter = {'id': result[0], 'key_word': result[1]}
        filters.append(filter)
    return filters

def get_all_filters():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM email_filters")
    results = cur.fetchall()
    if results is None:
        return None
    filters = []
    for result in results:
        filter = {'key_word': result[1], 'email': result[2]}
        filters.append(filter)
    return filters

def get_count_filters_per_user(email):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM email_filters WHERE email = ?", (email,))
    results = cur.fetchall()
    return len(results)