import sqlite3

# Connect to database (will be created if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table with premium field if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    language TEXT DEFAULT 'en',
    premium INTEGER DEFAULT 0
)
''')
conn.commit()

# Safe auto-migration: add 'premium' column if missing
cursor.execute("PRAGMA table_info(users)")
columns = [col[1] for col in cursor.fetchall()]
if "premium" not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN premium INTEGER DEFAULT 0")
    conn.commit()

def set_user_language(user_id, language):
    cursor.execute('''
        INSERT INTO users (user_id, language, premium)
        VALUES (?, ?, COALESCE((SELECT premium FROM users WHERE user_id = ?), 0))
        ON CONFLICT(user_id) DO UPDATE SET language=excluded.language
    ''', (user_id, language, user_id))
    conn.commit()

def get_user_language(user_id):
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 'en'

# ✅ NEW: Set user as premium (1 = True, 0 = False)
def set_user_premium(user_id, is_premium=True):
    cursor.execute('''
        INSERT INTO users (user_id, language, premium)
        VALUES (?, 'en', ?)
        ON CONFLICT(user_id) DO UPDATE SET premium=excluded.premium
    ''', (user_id, int(is_premium)))
    conn.commit()

# ✅ NEW: Check if user is premium
def is_user_premium(user_id):
    cursor.execute('SELECT premium FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    return result[0] == 1 if result else False
