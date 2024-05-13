from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from models import Users
from starlette import status
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime,timedelta
from pydantic import Field, BaseModel

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

ALGORITHM = "HS256"
SECRET_KEY = "hahahhahshsbxbhsbxjaj33b3bhchfbhh"

router = APIRouter(
    prefix="/auth",
    tags = ["Authorization Landing Page"]
)

class Token(BaseModel):
    access_token: str
    token_type: str

class CreateUserRequest(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length = 1)
    email: str
    password: str
    username: str
    role: str

bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

'''
def authenticate_user(username:str, password:str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if user is None:
        return False
    if not bcrypt_context.verify(user.hashed_password, password):
        print(user.hashed_password)
        print(password)
        return False

    return user
'''

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()

    if user is None:
        print("User not found:", username)
        return False

    print("Retrieved hashed password from database:", user.hashed_password)
    print("Password provided during authentication:", password)

    if not bcrypt_context.verify(password, user.hashed_password):
        print("Passwords do not match.")
        return False

    return user



def create_access_token(username: str, id: int, role: str, expires_delta: timedelta):
    encode = {"sub":username, "id":id, "role":role}
    expires_time = datetime.utcnow() + expires_delta
    encode.update({"exp": expires_time})

    return jwt.encode(encode,SECRET_KEY, algorithm= ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        username: str = payload.get("sub")
        id: int = payload.get("id")
        role: str = payload.get("role")

        return {"username": username, "id": id, "role": role}

    except JWTError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "JWT Error")    




@router.post("/", status_code = status.HTTP_201_CREATED)
async def create_new_user(user: CreateUserRequest,
                          db: db_dependency):
    user_model = Users(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        hashed_password = bcrypt_context.hash( user.password),
        role = user.role,
        is_active = True,
        username = user.username
    )

    db.add(user_model)
    db.commit()

    return user_model

@router.post("/token", response_model = Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    
    user = authenticate_user(form_data.username,form_data.password,db)

    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Authentication Failed")
    
    token = create_access_token(user.username,user.id,user.role,timedelta(minutes = 20))


    return {"access_token": token, "token_type":"bearer"}



