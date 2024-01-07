import sqlite3

db_name="telegram_stats_db.db"


def create_users_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            phone TEXT,
            name TEXT, 
            username TEXT
             
        )
    ''')

    conn.commit()
    conn.close()

