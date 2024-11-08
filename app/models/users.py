# app/models/users.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from pydantic import BaseModel
from sqlalchemy.orm import validates
import re

# SQLAlchemy model for database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    nickname = Column(String, nullable=True)  # Optional field
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive

    urls = relationship("URL", back_populates="user")

    @validates('email')
    def validate_email(self, key, value):
        # Simple email validation using regex
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email address")
        return value

# Pydantic model for base data structure
class UserBase(BaseModel):
    email: str
    nickname: str | None = None

# Pydantic model for creating the User entry (request model)
class UserCreate(BaseModel):
    email: str
    password: str
    confirm_password: str
    nickname: str | None = None

    class Config:
        # Ensure that the password is not sent in the response
        from_attributes = True

# Pydantic model for returning the User entry (response model)
class UserResponse(UserBase):
    id: int
    is_active: int

    class Config:
        from_attributes = True

class UserRequest(BaseModel):
    email: str
    password: str
