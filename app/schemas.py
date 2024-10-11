from pydantic import BaseModel
from typing import List, Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class ItemBase(BaseModel):
    item_name: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    is_done: bool

    class Config:
        orm_mode = True

class ChecklistBase(BaseModel):
    name: str

class ChecklistCreate(ChecklistBase):
    pass

class Checklist(ChecklistBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
