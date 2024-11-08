# services/url_service.py

from sqlalchemy.orm import Session
from app.models.url import URL
from app.schemas.url import URLCreate
import random
import string

def generate_short_url(length: int = 6) -> str:
    """Generate a random short URL."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_url(db: Session, url_create: URLCreate) -> URL:
    """Create and store a new short URL in the database."""
    short_url = generate_short_url()
    
    # Ensure the short URL is unique by checking the database
    while db.query(URL).filter(URL.short_url == short_url).first():
        short_url = generate_short_url()

    db_url = URL(original_url=url_create.original_url, short_url=short_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url(db: Session, short_url: str) -> str:
    # Query the database for the short URL
    url = db.query(URL).filter(URL.short_url == short_url).first()
    if url:
        url.clicks += 1  # Increment click count
        db.commit()
        return url.original_url  # Return the original URL if found
    return None  # Return None if not found
