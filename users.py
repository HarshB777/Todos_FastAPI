from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException
from .todos import get_db, db_dependency,user_dependency
from .auth import get_current_user,bcrypt_context
from starlette import status
from models import Users


router = APIRouter(
    prefix = "/users",
    tags = ["User Requests Landing Page"]
)


class PasswordChange(BaseModel):
    password: str
    new_password: str = Field(min_length = 4)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_curr_user_details(user: user_dependency,
                                db: db_dependency):
    
    if not user:
        raise HTTPException(status_code=401, detail = "User is unauthorized")
    
    return db.query(Users).filter(user.get("id") == Users.id).first()



@router.put("/password", status_code=status.HTTP_201_CREATED)
async def change_password(user: user_dependency,
                          db: db_dependency,
                          request: PasswordChange):
    if not user:
        raise HTTPException(status_code=401, detail = "User is unauthorized")
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt_context.verify(request.password,user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Password verification failed")
    
    user_model.hashed_password = bcrypt_context.hash(request.new_password)

    db.add(user_model)
    db.commit()


    
    

