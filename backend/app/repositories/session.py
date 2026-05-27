from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.session import Session as ChatSession
from app.schemas.session import SessionCreate

def create(db: Session, session_in: SessionCreate) -> ChatSession:
    db_session = ChatSession(
        user_id=session_in.user_id,
        title=session_in.title,
        messages=[]
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_by_id(db: Session, session_id: int) -> ChatSession | None:
    return db.get(ChatSession, session_id)

def get_all_by_user_id(db: Session, user_id: int) -> list[ChatSession]:
    query = select(ChatSession).where(ChatSession.user_id == user_id).order_by(ChatSession.created_at.desc())
    return list(db.scalars(query).all())

def update_messages(db: Session, db_session: ChatSession, messages: list[dict]) -> ChatSession:
    db_session.messages = messages
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def update_title(db: Session, db_session: ChatSession, title: str) -> ChatSession:
    db_session.title = title
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def delete(db: Session, id: int) -> bool:
    db_session = get_by_id(db, id)
    if not db_session:
        return False
    db.delete(db_session)
    db.commit()
    return True

