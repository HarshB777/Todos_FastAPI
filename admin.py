from fastapi import APIRouter, Depends, HTTPException
from .auth import get_current_user
from models import Users,Todos
from passlib.context import CryptContext
from starlette import status
from .auth import get_db, db_dependency,bcrypt_context
from .todos import user_dependency




router = APIRouter(
    prefix = "/admin",
    tags = ["Admin's Landing Page"]
)


#GET - all todos
@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_user_details(user: user_dependency,
                           db: db_dependency):
    
    if not user or user.get("role")!="admin":
        raise HTTPException(status_code=401, detail = "User is unauthorized")

    return db.query(Todos).all()

#GET - all users
@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(user:user_dependency,db: db_dependency):
    if not user or user.get("role") != "admin":
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "User is unauthorized")
    return db.query(Users).all()