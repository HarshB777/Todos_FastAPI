from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from .auth import get_current_user
from starlette import status
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic import BaseModel, Field
from models import Todos

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


class TodosRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length = 200)
    priority: int = Field(gt = 0, lt = 11)
    complete: bool



router = APIRouter(
    prefix = "/todos",
    tags = ["Todos Landing Page"]
)

user_dependency = Annotated[dict,Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]


#GET - say hello to a given user
@router.get("/hello")
async def say_hello(user: user_dependency):
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User Authentication Failed")
    
    return "Hello"

#GET - return all todo items for a given user
@router.get("/",status_code = status.HTTP_200_OK)
async def get_all_todos(user: user_dependency,
                        db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "User Authentication Failed")
    
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


#GET - get todo item by id
@router.get("/{todo_id}", status_code = status.HTTP_200_OK)
async def get_todo_by_id(user: user_dependency,
                         db: db_dependency,
                         todo_id: int):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "User Authorization failed!")

    todo_item = db.query(Todos).filter(todo_id == Todos.id).filter(user.get("id") == Todos.owner_id).first()

    if not todo_item:
        raise HTTPException(status_code = 404, detail = "Todo item not found")
    
    return todo_item




#POST - Create a new item in todo for a given user
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_todo(user: user_dependency,
                          db: db_dependency,
                          todo_request: TodosRequest):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "User Authentication Failed")
    
    todo_model = Todos(**todo_request.dict(), owner_id = user.get("id"))

    db.add(todo_model)
    db.commit()

    return "Todo item is added!"
    

#PUT - Update a given item in todo for a user
@router.put("/{todo_id}", status_code= status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,
                      db: db_dependency,
                      todo_request: TodosRequest,
                      todo_id: int):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "User is Not Authorized")
    
    curr_item = db.query(Todos).filter(todo_id == Todos.id).filter(Todos.owner_id == user.get("id")).first()
    
    if curr_item is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Todo item not found")
        
    curr_item.title = todo_request.title
    curr_item.description = todo_request.description
    curr_item.priority = todo_request.priority
    curr_item.complete = todo_request.complete

    db.add(curr_item)
    db.commit()

    return "Todo item is now updated!"



#DELETE - delete a given item in todo for a user
@router.delete("/{todo_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_todoid(user: user_dependency,
                        db: db_dependency,
                        todo_id: int):
    
    if user is None:
        raise HTTPException(status_code=404, detail="User Authentication Failed")
    
    todo_item = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()

    if todo_item is None:
        raise HTTPException(status_code=404, detail = "Todo item not found!")


    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).delete()
    db.commit()

    
