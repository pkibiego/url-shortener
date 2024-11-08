# main.py

from fastapi import FastAPI, Depends
from app.api.routes import router
from app.db.database import Base, engine, SessionLocal, get_db
from app.schemas.url import URLCreate, URLResponse
from app.models.url import URL
from sqlalchemy.orm import Session

async def lifespan(app: FastAPI):
    # Create tables on startup
    Base.metadata.create_all(bind=engine)
    yield
    # You can also include shutdown events here if needed

app = FastAPI(lifespan=lifespan)

@app.post("/urls/", response_model=URLResponse)
def create_url(url: URLCreate, db: Session = Depends(get_db)):
    db_url = URL(original_url=url.original_url, short_url="short_link")  # Replace "short_link" with actual logic
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

@app.get("/")
async def read_root():
    return {"message": "Welcome to the URL Shortener API"}
