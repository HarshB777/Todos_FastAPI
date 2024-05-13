from database import engine
import models
from fastapi import FastAPI
from routers import auth,todos,admin,users


models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)