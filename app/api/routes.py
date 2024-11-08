from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse  # Import for redirection
from app.db.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services.url_service import create_url, get_url

router = APIRouter()

@router.post("/shorten/", response_model=URLResponse)
def shorten_url(url: URLCreate, db: Session = Depends(get_db)):
    return create_url(db=db, url_create=url)

@router.get("/{short_url}")
def redirect_url(short_url: str, db: Session = Depends(get_db)):
    """Redirect to the original URL using the shortened URL"""
    # Fetch the original URL from the database
    original_url = get_url(db=db, short_url=short_url)

    if not original_url:
        return {"error": "Shortened URL not found"}  # Handle case when short URL is not found
    
    # Redirect to the original URL
    return RedirectResponse(url=original_url)