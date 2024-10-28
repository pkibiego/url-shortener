from sqlalchemy.orm import Session
from app.models.url import URL
from app.schemas.url import URLCreate
import random
import string

def generate_short_url(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_url(db: Session, url_create: URLCreate) -> URL:
    short_url = generate_short_url()
    db_url = URL(original_url=url_create.original_url, short_url=short_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url(db: Session, short_url: str):
    db_url = db.query(URL).filter(URL.short_url == short_url).first()
    if db_url:
        db_url.clicks += 1
        db.commit()
    return db_url
