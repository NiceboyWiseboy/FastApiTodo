import models
from database import engine
from routers import auth, todos, users, address
from fastapi import FastAPI


app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(address.router)
models.Base.metadata.create_all(bind=engine)
