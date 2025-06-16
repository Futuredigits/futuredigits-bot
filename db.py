import sqlite3

# Connect to database (will be created if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    language TEXT DEFAULT 'en'
)
''')
conn.commit()


def set_user_language(user_id, language):
    cursor.execute('REPLACE INTO users (user_id, language) VALUES (?, ?)', (user_id, language))
    conn.commit()


def get_user_language(user_id):
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 'en'
