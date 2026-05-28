import os
import sys
from sqlalchemy import text

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.core.database import analytics_engine

def test_analytics():
    if analytics_engine is None:
        print("Analytics engine is not configured.")
        return
    
    try:
        with analytics_engine.connect() as conn:
            result = conn.execute(text("SELECT count(*) FROM customers"))
            count = result.scalar()
            print(f"Successfully connected to Analytics DB. Customer count: {count}")
    except Exception as e:
        print(f"Error connecting to Analytics DB: {e}")

if __name__ == "__main__":
    test_analytics()
