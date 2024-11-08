# app/services/user_service.py

from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.user import UserCreate

# Function to create a new user
def create_user(db: Session, user_create: UserCreate) -> User:
    """Create a new user in the database."""
    db_user = User(
        email=user_create.email,
        hashed_password=user_create.hashed_password,
        nickname=user_create.nickname
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Function to get a user by their email
def get_user_by_email(db: Session, email: str) -> User:
    """Retrieve a user from the database by email."""
    return db.query(User).filter(User.email == email).first()