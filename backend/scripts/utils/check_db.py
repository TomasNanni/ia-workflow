import sqlite3
import os

# Resolve path to sessions.db relative to backend root
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../sessions.db"))

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email FROM users")
    users = cursor.fetchall()
    print(f"Users: {users}")
    
    cursor.execute("SELECT id, user_id, title FROM sessions")
    sessions = cursor.fetchall()
    print(f"Sessions: {sessions}")
    conn.close()
except Exception as e:
    print(f"Error connecting to {db_path}: {e}")
