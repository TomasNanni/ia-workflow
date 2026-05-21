from datetime import datetime
from pydantic import BaseModel, ConfigDict

class SessionBase(BaseModel):
    title: str

class SessionCreate(SessionBase):
    user_id: int

class SessionRead(SessionBase):
    id: int
    user_id: int
    created_at: datetime
    messages: list[dict]
    model_config = ConfigDict(from_attributes=True)
