import hashlib
import sqlite3

def connect_db():
    connection = sqlite3.connect('database/database.db')
    connection.row_factory = sqlite3.Row
    return connection

def retrieve_site_id(site_title):
    conn = connect_db()

    try:
        cur = conn.cursor()

        cur.execute("SELECT id FROM sites WHERE site_title = ?", (site_title,))
        conn.commit()
        site_data = cur.fetchone()

        if not site_data:
            print("retrieve_site_id error: no matching site found")
            return None

        return site_data['id']

    finally:
        conn.close()

def get_hash(title):
    hash_object = hashlib.sha256(title.encode('utf-8'))
    hex_digest = hash_object.hexdigest()

    hash_bytes = bytes.fromhex(hex_digest)

    return hash_bytes