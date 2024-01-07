import sqlite3
from datetime import datetime, timedelta

db_name="telegram_stats_db.db"

# Get user info or if not exist user phone using user_id
def get_username_or_phone(user_id):
    conn = sqlite3.connect(db_name)  
    cursor = conn.cursor()

    cursor.execute('SELECT username, phone FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()

    conn.close()

    if user_data:
        username, phone = user_data
        return username if username else phone
    else:
        return None 

# Get message type for each user from meesages 
def get_message_statistics():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT user_id, message_type, COUNT(*) as total_count
        FROM messages
        GROUP BY user_id, message_type
        ORDER BY total_count DESC
    ''')

    rows = cursor.fetchall()

    result = {}
    for row in rows:
        user_id, message_type, total_count = row
        if user_id not in result:
            result[user_id] = []
        result[user_id].append({'message_type': message_type, 'total_count': total_count})
    conn.close()
    return result

# Get amount of all messages
def get_message_amount():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COUNT(*) as total_count
        FROM messages
    ''')

    rows = cursor.fetchall()

    conn.close()
    return rows[0]

# Get chat name
def get_chat_name():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT chat_title
        FROM chats
    ''')

    rows = cursor.fetchall()

    conn.close()
    return rows[0]


# Get total duration of all audio and round video messages
def get_total_duration():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT user_id, SUM(CASE WHEN message_type = 'Audio' THEN duration ELSE 0 END) as audio_duration,
                           SUM(CASE WHEN message_type = 'Round Video' THEN duration ELSE 0 END) as video_duration
        FROM messages
        GROUP BY user_id
    ''')

    rows = cursor.fetchall()

    result = {}
    for row in rows:
        user_id, audio_duration, video_duration = row
        result[user_id] = {'audio_duration': audio_duration, 'video_duration': video_duration}

    conn.close()
    return result    

# Get and calculate messages by type for each user and sort
def get_top_message_types():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT message_type, COUNT(*) as message_count
        FROM messages
        GROUP BY message_type
        ORDER BY message_count DESC
    ''')

    rows = cursor.fetchall()

    result = []
    for row in rows:
        message_type, message_count = row
        result.append({'message_type': message_type, 'message_count': message_count})

    conn.close()
    return result

# Get and calculate messages by type for each user per period
def get_top_message_types_date(start_date, end_date):
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT message_type, COUNT(*) as message_count
        FROM messages
        WHERE date_sent BETWEEN ? AND ?
        GROUP BY message_type
        ORDER BY message_count DESC
    ''', (start_date, end_date))

    rows = cursor.fetchall()

    result = []
    for row in rows:
        message_type, message_count = row
        result.append({'message_type': message_type, 'message_count': message_count})

    conn.close()
    return result
    
# Get calculated frequency of sending messages distincted by type for wach user (per hour per period)  
def get_message_type_frequency_per_hour(start_date, end_date):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT user_id, message_type, COUNT(*) as message_count
        FROM messages
        WHERE date_sent BETWEEN ? AND ?
        GROUP BY user_id, message_type
        ORDER BY user_id, message_type
    ''', (start_date, end_date))

    rows = cursor.fetchall()

    result = {}
    for row in rows:
        user_id, message_type, message_count = row

        if user_id not in result:
            result[user_id] = {}

        result[user_id][message_type] = message_count

    conn.close()
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')   

    for user_id, user_data in result.items():
        total_hours = (end_date - start_date).total_seconds() / 3600
        for message_type, message_count in user_data.items():
            user_data[message_type] = message_count / total_hours

    return result    

# Get calculated frequency of sending messages for each user(per hour per period)  
def get_total_message_frequency_per_hour_notype(start_date, end_date):

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT user_id, COUNT(*) as message_count
        FROM messages
        WHERE date_sent BETWEEN ? AND ?
        GROUP BY user_id
        ORDER BY user_id
    ''', (start_date, end_date))

    rows = cursor.fetchall()

    result = {}
    for row in rows:
        user_id, message_count = row
        result[user_id] = message_count
 
    conn.close()
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')  
    # Рассчитываем частоту в час
    total_hours = (end_date - start_date).total_seconds() / 3600
    for user_id, message_count in result.items():
        result[user_id] = message_count / total_hours

    return result

# Get calculated frequency of sending messages distincted by type  (per hour per period)  
def get_message_type_frequency_per_hour_nouser(start_date, end_date):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT message_type, COUNT(*) as message_count
        FROM messages
        WHERE date_sent BETWEEN ? AND ?
        GROUP BY message_type
        ORDER BY message_type
    ''', (start_date, end_date))

    rows = cursor.fetchall()

    result = {}
    for row in rows:
        message_type, message_count = row
        result[message_type] = message_count

    conn.close()
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')  

    total_hours = (end_date - start_date).total_seconds() / 3600
    for message_type, message_count in result.items():
        result[message_type] = message_count / total_hours

    return result

# Get calculated frequency of sending messages  (per hour per period)  
def get_total_message_frequency_per_hour_all(start_date, end_date):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT COUNT(*) as total_message_count
        FROM messages
        WHERE date_sent BETWEEN ? AND ?
    ''', (start_date, end_date))
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d') 
    total_messages = cursor.fetchone()[0]
    total_hours = (end_date - start_date).total_seconds() / 3600
    total_frequency_per_hour = total_messages / total_hours

    conn.close()
    return total_frequency_per_hour
