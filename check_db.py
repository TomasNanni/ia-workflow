import sqlite3

try:
    conn = sqlite3.connect("backend/sessions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, email FROM users")
    users = cursor.fetchall()
    print(f"Users: {users}")
    
    cursor.execute("SELECT id, user_id, title FROM sessions")
    sessions = cursor.fetchall()
    print(f"Sessions: {sessions}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
