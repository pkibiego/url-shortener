from fastapi import FastAPI, Depends, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.api.routes import router
from app.db.database import Base, engine, SessionLocal, get_db
from app.schemas.url import URLCreate, URLResponse
from app.models.url import URL
from sqlalchemy.orm import Session
from app.services.url_service import generate_short_url, get_url
from app.schemas.user import UserCreate
from app.models.users import User
from app.services.user_service import create_user
from app.auth.authentication import hash_password, get_user_by_email, verify_jwt_token, create_access_token, verify_password
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# App initialization
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "app" / "static"), name="static")

# Helper function to check user authentication
def is_user_authenticated(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return False
    try:
        verify_jwt_token(token.split(" ")[1])
        return True
    except Exception:
        return False

# Index route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    user_authenticated = is_user_authenticated(request)

    # Redirect to /landing if the user is already logged in
    if user_authenticated:
        return RedirectResponse(url="/landing")

    return templates.TemplateResponse("index.html", {"request": request, "user_authenticated": user_authenticated})

# Registration route
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "user_authenticated": False})

@app.post("/register")
async def register_user(
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    nickname: str = Form(None),
    db: Session = Depends(get_db)
):
    if password != confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(password)
    user_create = UserCreate(email=email, hashed_password=hashed_password, nickname=nickname)
    user = create_user(db, user_create)
    return {"message": "User registered successfully", "user_id": user.id}

# Login route
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user_authenticated = is_user_authenticated(request)
    return templates.TemplateResponse("login.html", {"request": request, "user_authenticated": user_authenticated})

"""
@app.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/landing", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return response

# Logout route
@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response

# Landing page
@app.get("/landing", response_class=HTMLResponse)
async def landing(request: Request, db: Session = Depends(get_db)):
    user_authenticated = is_user_authenticated(request)
    if not user_authenticated:
        return RedirectResponse(url="/login")

    try:
        token = request.cookies.get("access_token")
        payload = verify_jwt_token(token.split(" ")[1])
        user_email = payload.get("sub")
        user = get_user_by_email(db, user_email)

        if not user:
            return RedirectResponse(url="/login")

        user_links = db.query(URL).filter(URL.user_id == user.id).order_by(URL.id.desc()).limit(5).all()

        return templates.TemplateResponse(
            "landing.html",
            {
                "request": request,
                "user": user,
                "links": user_links,
                "user_authenticated": user_authenticated,
            }
        )

    except Exception as e:
        print(f"Error: {e}")
        return RedirectResponse(url="/login")
"""

# URL redirection route
@app.get("/{short_url}")
async def redirect_to_original(short_url: str, db: Session = Depends(get_db)):
    # Retrieve the original URL from the database
    original_url = get_url(db=db, short_url=short_url)

    # If the short URL doesn't exist, redirect to homepage
    if not original_url:
        return RedirectResponse(url="/")
    
    # If found, redirect to the original URL
    return RedirectResponse(url=original_url)

@app.get("/{path_name:path}")
async def catch_all(path_name: str):
    return RedirectResponse(url="/")
