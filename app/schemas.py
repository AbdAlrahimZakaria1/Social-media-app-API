from pydantic import BaseModel
from datetime import datetime
from pydantic.networks import EmailStr


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

    # class Config:
    #     orm_mode = True


class postOut(BaseModel):
    Post: Post
    votes: int

    # class Config:
    #     orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int


class Vote(BaseModel):
    post_id: int
    vote_dir: int
