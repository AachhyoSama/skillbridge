# Schema for request response models
from pydantic import BaseModel, EmailStr
from typing import List, Optional


class RegisterUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    bio: Optional[str] = None
    skills_offered: List[str] = []
    skills_wanted: List[str] = []


class UserBase(BaseModel):
    email: EmailStr
    username: str
    bio: Optional[str] = None
    skills_offered: List[str] = []
    skills_wanted: List[str] = []


class UserPublic(UserBase):
    id: str  # stringified ObjectId for frontend


class UserInDB(UserBase):
    hashed_password: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# to update the user
class UpdateUser(BaseModel):
    username: Optional[str]
    bio: Optional[str]
    skills_offered: Optional[List[str]]
    skills_wanted: Optional[List[str]]
