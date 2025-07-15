import sqlite3
import os
import logging

logging.basicConfig(level=logging.DEBUG)

db_path = os.path.abspath("users.db")
logging.debug(f"Using database at: {db_path}")
conn = sqlite3.connect(db_path)

cursor = conn.cursor()

# Create users table with premium + created_at fields if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    language TEXT DEFAULT 'en',
    premium INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
)
''')
conn.commit()

# Safe auto-migration: add 'premium' column if missing
cursor.execute("PRAGMA table_info(users)")
columns = [col[1] for col in cursor.fetchall()]
if "premium" not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN premium INTEGER DEFAULT 0")
    conn.commit()

# Safe auto-migration: add 'created_at' column if missing
cursor.execute("PRAGMA table_info(users)")
columns = [col[1] for col in cursor.fetchall()]
if "created_at" not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN created_at TEXT DEFAULT (datetime('now'))")
    conn.commit()

def set_user_language(user_id, language):
    cursor.execute('''
        INSERT INTO users (user_id, language, premium, created_at)
        VALUES (
            ?, ?, 
            COALESCE((SELECT premium FROM users WHERE user_id = ?), 0),
            COALESCE((SELECT created_at FROM users WHERE user_id = ?), datetime('now'))
        )
        ON CONFLICT(user_id) DO UPDATE SET language=excluded.language
    ''', (user_id, language, user_id, user_id))
    conn.commit()

def get_user_language(user_id):
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 'en'

# ✅ Set user as premium and preserve created_at
def set_user_premium(user_id, is_premium=True):
    cursor.execute('''
        INSERT INTO users (user_id, language, premium, created_at)
        VALUES (
            ?, 
            COALESCE((SELECT language FROM users WHERE user_id = ?), 'en'), 
            ?, 
            COALESCE((SELECT created_at FROM users WHERE user_id = ?), datetime('now'))
        )
        ON CONFLICT(user_id) DO UPDATE SET premium=excluded.premium
    ''', (user_id, user_id, int(is_premium), user_id))
    conn.commit()

# ✅ Check if user is premium
def is_user_premium(user_id):
    cursor.execute('SELECT premium FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    logging.debug(f"Premium check for user {user_id}: {result}")
    return result[0] == 1 if result else False

# ✅ Optional: Get user creation date
def get_user_created_at(user_id):
    cursor.execute("SELECT created_at FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY,
                  language TEXT,
                  is_premium INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def set_language(user_id: int, language_code: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (user_id, language) VALUES (?, ?)", (user_id, language_code))
    conn.commit()
    conn.close()

