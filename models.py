from database import Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index= True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    hashed_password = Column(String)

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
