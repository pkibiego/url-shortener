from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services.url_service import create_url, get_url

router = APIRouter()

@router.post("/shorten/", response_model=URLResponse)
def shorten_url(url: URLCreate, db: Session = Depends(get_db)):
    return create_url(db=db, url_create=url)

@router.get("/{short_url}", response_model=URLResponse)
def redirect_url(short_url: str, db: Session = Depends(get_db)):
    return get_url(db=db, short_url=short_url)
