from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime
from app.core.models import RoleEnum, ChildStatus

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.scout

class UserUpdatePassword(BaseModel):
    new_password: str = Field(min_length=6)

class ChildBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    birth_year: Optional[int] = None
    parent_name: Optional[str] = None
    phone: Optional[str] = None
    status: ChildStatus = ChildStatus.aktiv

class ChildCreate(ChildBase):
    pass

class ChildOut(ChildBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ReportCreate(BaseModel):
    child_id: int
    text: str

class ReportOut(BaseModel):
    id: int
    child_id: int
    author_id: int
    text: str
    created_at: datetime
    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    title: str
    address: Optional[str] = None
    date: datetime
    link: Optional[str] = None
    description: Optional[str] = None

class EventOut(EventCreate):
    id: int
    class Config:
        from_attributes = True

class AttendanceCreate(BaseModel):
    status: str = "zugesagt"