from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.session import SessionRead, SessionCreate
from app.services import session as session_service
from app.services import chat as chat_service
from app.services.auth import get_current_user
from app.models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/sessions", tags=["sessions"])

class ChatRequest(BaseModel):
    message: str

@router.get("/", response_model=list[SessionRead])
def list_sessions(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Listar todas las sesiones del usuario actual.
    """
    return session_service.get_user_sessions(db, current_user.id)

@router.post("/", response_model=SessionRead)
def create_session(
    session_in: SessionCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Crear una nueva sesión de chat.
    """
    # Forzar que el user_id sea el del usuario autenticado
    session_in.user_id = current_user.id
    return session_service.create_session(db, session_in)

@router.get("/{session_id}", response_model=SessionRead)
def get_session(
    session_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Obtener una sesión específica por ID.
    """
    session = session_service.get_session(db, session_id)
    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta sesión"
        )
    return session

@router.post("/{session_id}/chat")
async def chat(
    session_id: int, 
    request: ChatRequest, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Enviar un mensaje de chat a la IA y obtener una respuesta.
    """
    # Verificar propiedad de la sesión
    session = session_service.get_session(db, session_id)
    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para interactuar con esta sesión"
        )
    
    result = await chat_service.process_chat_message(db, session_id, request.message)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Error al procesar el mensaje"
        )
    
    return result

@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Eliminar una sesión específica por ID.
    """
    session_service.delete_session(db, session_id, current_user.id)
    return None

