from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.core.config import settings
from app.repositories import session as session_repo
from app.services.agent import agent, generate_session_title
from pydantic_ai.messages import ModelMessage, ModelResponse, ModelRequest, UserPromptPart, TextPart
import json

# Analytics engine (read-only)
analytics_engine = create_engine(settings.analytics_db_url)

async def process_chat_message(db: Session, session_id: int, user_message: str):
    # 1. Get session
    db_session = session_repo.get_by_id(db, session_id)
    if not db_session:
        return None

    # 2. Prepare history for pydantic-ai
    # Note: For MVP, we might just pass the last message or a limited history
    # The PRD says "stateless manner (no history context per query)" for the agent,
    # but we store the history for the user.
    # Actually, the PRD says: "History is for user reference only; the AI agent operates in a stateless manner (no history context per query)."
    # So we don't need to pass history to the agent.
    
    # 3. Run agent
    result = await agent.run(user_message, deps=analytics_engine)
    
    # 4. Extract data
    # result.data is the natural language response
    # We might want to find if any SQL was executed. 
    # pydantic-ai doesn't easily expose the tool calls in the final result.data unless we use a custom result type.
    # However, for this task, we can just return the result.data.
    
    # 5. Update session messages
    new_messages = db_session.messages.copy()
    new_messages.append({"role": "user", "content": user_message})
    new_messages.append({"role": "assistant", "content": result.data})
    
    session_repo.update_messages(db, db_session, new_messages)
    
    # 6. Generate title if it's the first message or title is default
    if db_session.title == "Nuevo Chat" or not db_session.title:
        try:
            new_title = await generate_session_title(user_message)
            session_repo.update_title(db, db_session, new_title)
        except Exception:
            # Silently fail for title generation to not break the chat
            pass
    
    return {
        "answer": result.data,
        "session_id": session_id,
        "messages": new_messages
    }
