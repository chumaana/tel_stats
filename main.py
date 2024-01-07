import sqlite3

from gui import login_gui
from db import chats, messages, users

# Delete all records from tables
def clear_table():
    conn = sqlite3.connect('telegram_stats_db.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM messages')
    cursor.execute('DELETE FROM chats')
    cursor.execute('DELETE FROM users')

    conn.commit()
    conn.close()
    
# Main function to initialize necessary tables and launch login GUI
def main():
    chats.create_chats_table()
    messages.create_messages_table()
    users.create_users_table()
    login_gui.create_login_window()
    clear_table()

if __name__ == "__main__":
    main()
