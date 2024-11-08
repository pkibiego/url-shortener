# main.py

from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.api.routes import router
from app.db.database import Base, engine, SessionLocal, get_db
from app.schemas.url import URLCreate, URLResponse
from app.models.url import URL
from sqlalchemy.orm import Session
from app.services.url_service import generate_short_url, get_url
from app.api.routes import router
from fastapi.staticfiles import StaticFiles
from pathlib import Path

async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield
    # You can also include shutdown events here if needed

app = FastAPI(lifespan=lifespan)

# Include the router with the defined routes
app.include_router(router, prefix="/api")  # This adds the routes under "/api"

templates = Jinja2Templates(directory="app/templates")
# Serve static files from the 'static' directory
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "app" / "static"), name="static")

@app.post("/urls/", response_model=URLResponse)
def create_url(url: URLCreate, db: Session = Depends(get_db)):
    db_url = URL(original_url=url.original_url, short_url=generate_short_url())  # Replace "short_link" with actual logic
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

"""
@app.get("/")
async def read_root():
    return {"message": "Welcome to the URL Shortener API"}
"""

url_mapping = {}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/shorten-url", response_model=URLResponse)
async def shorten_url(url_create: URLCreate, db: Session = Depends(get_db)):
    db_url = create_url(db=db, url_create=url_create)
    
    # Check if the URL was saved successfully
    if db_url:
        return URLResponse(id=db_url.id, original_url=db_url.original_url, short_url=db_url.short_url, clicks=db_url.clicks)
    else:
        return {"error": "Failed to shorten URL"}

@app.get("/{short_url}")
async def redirect_to_original(short_url: str, db: Session = Depends(get_db)):
    # Fetch the original URL from the database
    original_url = get_url(db=db, short_url=short_url)

    if not original_url:
        return {"error": "Shortened URL not found"}
    
    # Redirect to the original URL
    return RedirectResponse(url=original_url)