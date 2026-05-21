import os
import sys
from datetime import datetime, timedelta
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the current directory to sys.path to allow importing from app
sys.path.append(os.getcwd())

from app.core.config import settings
from app.core.database import Base
from app.models.user import User
from app.models.session import Session as ChatSession

def get_password_hash(password):
    # Hash a password for the first time
    # (Using bcrypt directly to avoid passlib issues)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def seed_data():
    print(f"Initializing SQLite database at {settings.sessions_db_url}...")
    
    # Ensure the engine uses the correct URL
    engine = create_engine(settings.sessions_db_url)
    SessionLocal = sessionmaker(bind=engine)
    
    # Create tables
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    db = SessionLocal()
    try:
        print("Seeding users...")
        users = []
        for i in range(1, 6):
            user = User(
                email=f"user{i}@example.com",
                hashed_password=get_password_hash(f"password{i}"),
                created_at=datetime.utcnow() - timedelta(days=30)
            )
            users.append(user)
        
        db.add_all(users)
        db.commit()
        
        # Get users back to use their IDs
        db_users = db.query(User).all()
        
        print("Seeding sessions...")
        sessions = []
        now = datetime.utcnow()
        
        for user in db_users:
            # Session from today
            sessions.append(ChatSession(
                user_id=user.id,
                title=f"Analysis for {user.email} - Today",
                created_at=now,
                messages=[
                    {"role": "user", "content": "Hello, how many sales did we have today?"},
                    {"role": "assistant", "content": "We had 5 sales today."}
                ]
            ))
            
            # Session from 2 days ago
            sessions.append(ChatSession(
                user_id=user.id,
                title=f"Previous Analysis - 2 days ago",
                created_at=now - timedelta(days=2),
                messages=[
                    {"role": "user", "content": "What was the top selling product yesterday?"},
                    {"role": "assistant", "content": "The top selling product was 'Laptop Pro 15'."}
                ]
            ))
            
            # Session from last week
            sessions.append(ChatSession(
                user_id=user.id,
                title=f"Historical Data Review",
                created_at=now - timedelta(days=7),
                messages=[
                    {"role": "user", "content": "List all customers from Madrid."},
                    {"role": "assistant", "content": "I found 3 customers from Madrid."}
                ]
            ))
            
        db.add_all(sessions)
        db.commit()
        print("Successfully seeded SQLite database with 5 users and 15 sessions!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
