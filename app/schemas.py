from pydantic import BaseModel
from datetime import datetime
from pydantic.networks import EmailStr
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: str


class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserOut


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
