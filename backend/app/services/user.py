from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import user as user_repo
from app.schemas.user import UserCreate
from app.services import auth as auth_service

def create_user(db: Session, user_in: UserCreate):
    if user_repo.get_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con este correo electrónico"
        )
    
    # Hash the password
    user_in_dict = user_in.model_dump()
    user_in_dict["password"] = auth_service.get_password_hash(user_in_dict["password"])
    
    # We can't pass the schema directly if we modified the password field in a dict
    # But user_repo.create expects UserCreate. 
    # Let's adjust user_repo.create to accept email and hashed_password or just dict.
    # Actually, it's better to keep repo pure and pass what it needs.
    
    return user_repo.create(db, user_in_dict)

def get_user(db: Session, user_id: int):
    user = user_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user
