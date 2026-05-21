from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.session import SessionRead, SessionCreate
from app.services import session as session_service

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.get("/", response_model=list[SessionRead])
def list_sessions(user_id: int = 1, db: Session = Depends(get_db)):
    """
    List all sessions for the current user.
    Hardcoded to user_id=1 until authentication is implemented.
    """
    return session_service.get_user_sessions(db, user_id)

@router.post("/", response_model=SessionRead)
def create_session(session_in: SessionCreate, db: Session = Depends(get_db)):
    """
    Create a new chat session.
    """
    return session_service.create_session(db, session_in)

@router.get("/{session_id}", response_model=SessionRead)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """
    Get a specific session by ID.
    """
    return session_service.get_session(db, session_id)
