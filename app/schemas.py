from pydantic import BaseModel
from datetime import datetime
from pydantic.networks import EmailStr
from typing import Optional


class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(BasePost):
    pass


class UpdatePost(BasePost):
    pass


class Post(BasePost):
    id: int
    created_at: datetime


class IgnoredType:
    pass


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
