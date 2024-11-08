# app/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str
    nickname: Optional[str] = None

    class Config:
        from_attributes = True
