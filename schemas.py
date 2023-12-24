from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Todo(BaseModel):
    todo: str
    
class File(BaseModel):
    file: str
    type: str
    

class Question(BaseModel):
    question: str

class Path(BaseModel):
    path: str
    

# Auth classes
class UserLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"


class UserBase(BaseModel):
    email: str
    username: str
    age: Optional[int] = None
    level: UserLevel = UserLevel.beginner


class UserIn(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str