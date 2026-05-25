import asyncio
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.session import Session as ChatSession
from app.models.user import User
from app.services import chat as chat_service
from app.repositories import session as session_repo

async def test_chat_service():
    # Setup test DB
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # Create test user
    user = User(email="test@example.com", hashed_password="hashed")
    db.add(user)
    db.commit()
    
    # Create test session
    session = ChatSession(user_id=user.id, title="Test Chat", messages=[])
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # Mock agent
    mock_result = MagicMock()
    mock_result.data = "Esta es una respuesta de la IA"
    
    chat_service.agent.run = AsyncMock(return_value=mock_result)
    
    print("Testing process_chat_message...")
    result = await chat_service.process_chat_message(db, session.id, "Hola")
    
    print(f"Result: {result}")
    assert result["answer"] == "Esta es una respuesta de la IA"
    assert len(result["messages"]) == 2
    assert result["messages"][0]["role"] == "user"
    assert result["messages"][1]["role"] == "assistant"
    
    # Verify DB update
    db.refresh(session)
    assert len(session.messages) == 2
    assert session.messages[1]["content"] == "Esta es una respuesta de la IA"
    
    print("Chat service test passed!")

if __name__ == "__main__":
    asyncio.run(test_chat_service())
