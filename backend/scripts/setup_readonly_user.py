import os
import psycopg2
from dotenv import load_dotenv

# Load .env from backend folder
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def setup_readonly_user():
    admin_url = os.getenv("DATABASE_URL")
    if not admin_url:
        print("Error: DATABASE_URL not found in .env")
        return

    # Extract credentials for the new user from ANALYTICS_DB_URL if possible, 
    # but we'll use the ones provided by the user manually for safety.
    new_user = "analytics_user"
    new_pass = "AnalyticsUserPassword"

    print(f"Connecting to Supabase as admin...")
    try:
        conn = psycopg2.connect(admin_url)
        conn.autocommit = True
        cur = conn.cursor()

        print(f"Creating user '{new_user}'...")
        try:
            cur.execute(f"CREATE USER {new_user} WITH PASSWORD '{new_pass}';")
        except psycopg2.errors.DuplicateObject:
            print(f"User '{new_user}' already exists, updating password...")
            cur.execute(f"ALTER USER {new_user} WITH PASSWORD '{new_pass}';")
        
        print("Granting permissions...")
        # Grant connect
        cur.execute(f"GRANT CONNECT ON DATABASE postgres TO {new_user};")
        # Grant usage on schema
        cur.execute(f"GRANT USAGE ON SCHEMA public TO {new_user};")
        # Grant select on all existing tables
        cur.execute(f"GRANT SELECT ON ALL TABLES IN SCHEMA public TO {new_user};")
        # Ensure future tables are also readable
        cur.execute(f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO {new_user};")

        print(f"Successfully configured '{new_user}' with read-only permissions!")
        
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_readonly_user()
