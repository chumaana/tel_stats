import sqlite3
db_name="telegram_stats_db.db"

def create_chats_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY,
            chat_id INTEGER,
            chat_title TEXT,
            chat_type TEXT
        )
    ''')

    conn.commit()
    conn.close()

def save_chat_to_db(chat):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO chats (chat_id, chat_title, chat_type)
        VALUES (?, ?, ?)
    ''', (chat.id, chat.title, chat.entity.__class__.__name__))

    conn.commit()
    conn.close()