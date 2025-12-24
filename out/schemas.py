from __future__ import annotations

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    is_active: bool


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
