from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

def create(db: Session, user_in: dict) -> User:
    db_user = User(
        email=user_in["email"],
        hashed_password=user_in["password"]
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

def get_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))
