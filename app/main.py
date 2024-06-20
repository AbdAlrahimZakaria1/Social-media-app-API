from fastapi import FastAPI

import psycopg2
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine
from .routers import users, posts, authentication

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authentication.router)

# This is the connection to the DB without sqlalchemy
# try:
#     connection = psycopg2.connect(
#         host="localhost",
#         database="fastapi",
#         user="postgres",
#         password="70336165",
#         cursor_factory=RealDictCursor,
#     )
#     cursor = connection.cursor()
#     print("Connection to database is successful!")
# except Exception as error:
#     print(f"Connection to database failed.\nerror: {error}")
