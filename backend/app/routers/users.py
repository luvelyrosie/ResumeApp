from typing import Annotated
from fastapi import APIRouter, Depends, Form, status, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from .pydantic_schemas import Token
from ..models import User
from ..database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


router=APIRouter(
    prefix="/user",
    tags=["user"]
)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

db_dependency=Annotated[Session, Depends(get_db)]
templates=Jinja2Templates(directory="frontend/templates")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/user/token")
bcrypt_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY='f0d6e9c1a5b8f72c3d4e5a96708b1c4a5f6e7d8c9a0b1c2d3e4f5a6b7c8d9e0f'
ALGORITHM='HS256'


def authenticate_user(username: str, password: str, db):
    user=db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_web_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode={
        "sub":username,
        "id":user_id,
        "role": role
    }
    expires=datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        role = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return {"username": username, "id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    
def get_current_user_cookie(request: Request):
    token = request.cookies.get("access_token")
    return decode_jwt(token)



def get_current_user_bearer(token: str = Depends(oauth2_bearer)):
    return decode_jwt(token)


user_dependency_cookie = Annotated[dict, Depends(get_current_user_cookie)]
user_dependency_bearer = Annotated[dict, Depends(get_current_user_bearer)]


@router.get("/register", response_class=HTMLResponse)
async def render_register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {"request": request})


@router.post("/register")
async def register_user(db: db_dependency,request: Request,email: EmailStr = Form(...),
                        username: str = Form(...),password: str = Form(...),role: str = Form("user")):
    user_exists = db.query(User).filter(User.email == email).first()
    if user_exists:
        return templates.TemplateResponse(request,"register.html",
            {"request": request, "error": "Email already registered, please login"}
        )
    
    user_model = User(
        email=email,
        username=username,
        role=role,
        hashed_password=bcrypt_context.hash(password)
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    
    token = create_web_token(user_model.username, user_model.id, user_model.role, timedelta(minutes=20))
    
    response = RedirectResponse(url="/resumes/", status_code=303)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response
    
    
@router.get("/login")
async def render_login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")


@router.post("/login")
async def login(db: db_dependency, request: Request, username: str = Form(...), 
                password: str = Form(...)):
    user = authenticate_user(username, password, db)
    if not user:
        return templates.TemplateResponse(request, "login.html", {"request": request, "error": "Invalid email or password"})
    
    token = create_web_token(user.username, user.id, user.role, timedelta(minutes=20))
    
    response = RedirectResponse(url="/resumes", status_code=303)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response


@router.post("/token", status_code=status.HTTP_201_CREATED, response_model=Token)
async def token_for_bearer(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user=authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Couldnt validate credentials')
    token=create_web_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {"access_token":token, "token_type":"bearer"}