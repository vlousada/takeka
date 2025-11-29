from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

class ObservationCreate(BaseModel):
    user_id: int
    target_name: str
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = None
