# app/models/url.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from pydantic import BaseModel

# SQLAlchemy model for database
class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_url = Column(String, unique=True, index=True)
    clicks = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="urls")

# Pydantic model for base data structure
class URLBase(BaseModel):
    original_url: str
    short_url: str

# Pydantic model for creating the URL entry (request model)
class URLCreate(BaseModel):
    original_url: str

# Pydantic model for returning the URL entry (response model)
class URLResponse(URLBase):
    clicks: int

    class Config:
        from_attributes = True

class URLRequest(BaseModel):
    original_url: str

