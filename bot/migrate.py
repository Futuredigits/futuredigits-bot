import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("ALTER TABLE users ADD COLUMN premium INTEGER DEFAULT 0")
conn.commit()

print("✅ Premium column added successfully.")
