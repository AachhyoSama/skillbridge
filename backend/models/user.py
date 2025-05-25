from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    email: EmailStr
    username: str
    hashed_password: str
    bio: Optional[str] = None
    skills_offered: list[str] = []
    skills_wanted: list[str] = []

    # tells Pydantic to treat ORM/mongo-like objects as dicts for serialization
    class Config:
        orm_mode = True
