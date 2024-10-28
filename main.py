from fastapi import FastAPI
from app.api.routes import router
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the URL Shortener API"}
