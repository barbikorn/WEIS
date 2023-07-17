from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id : Optional[str]
    name: str
    email: str
    password: str
    role: str
    age: int
    address: Optional[str] 

class UserUpdate(BaseModel):
    id : Optional[str]
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    role: Optional[str]
    age: Optional[int]
    address: Optional[str] 

