from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import session as session_repo
from app.schemas.session import SessionCreate

def create_session(db: Session, session_in: SessionCreate):
    return session_repo.create(db, session_in)

def get_session(db: Session, session_id: int):
    session = session_repo.get_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada"
        )
    return session

def get_user_sessions(db: Session, user_id: int):
    return session_repo.get_all_by_user_id(db, user_id)

def delete_session(db: Session, session_id: int, user_id: int):
    session = session_repo.get_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada"
        )
    
    if session.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta sesión"
        )
    
    return session_repo.delete(db, session_id)
