from fastapi import FastAPI

from . import models
from .database import engine
from .routers import users, posts, authentication, votes

# This is not needed anymore since the DB migrations are done by Alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)
app.include_router(authentication.router)
