from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import user as user_repo
from app.schemas.user import UserCreate

def create_user(db: Session, user_in: UserCreate):
    if user_repo.get_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    return user_repo.create(db, user_in)

def get_user(db: Session, user_id: int):
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
