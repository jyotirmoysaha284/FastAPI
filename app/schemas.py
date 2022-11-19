from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint

# Defining the schema of the Post/Request body
class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = 0


class ResponseUser(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    pass

class ResponsePost(PostBase):
    id: int
    rating: Optional[int]
    created_at: datetime
    owner_id: int
    owner: ResponseUser

    # Converts the SQLAlchemy model into a Pydantic model
    class Config:
        orm_mode = True

class ResponsePostWithVote(BaseModel):
    Post: ResponsePost
    vote_count: int

    # Converts the SQLAlchemy model into a Pydantic model
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserCredential(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)