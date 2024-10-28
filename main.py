from fastapi import FastAPI, Depends
from app.api.routes import router
from app.db.database import Base, engine, SessionLocal, get_db
from app.schemas.url import URLCreate, URLResponse
from app.models.url import URL
from sqlalchemy.orm import Session

app = FastAPI()

@app.on_event("startup")  # Corrected decorator
def on_startup():
    Base.metadata.create_all(bind=engine)

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
