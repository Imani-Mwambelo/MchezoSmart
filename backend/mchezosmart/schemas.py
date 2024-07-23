from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "user"

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    role: Optional[str]

class User(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class TontineBase(BaseModel):
    name: str
    start_date: date
    days_per_cycle: int
    interval:int
    number_of_members: int

class TontineCreate(TontineBase):
    creator_id: int

class TontineUpdate(BaseModel):
    name: Optional[str]
    start_date: Optional[date]
    days_per_cycle: Optional[int]
    number_of_members: Optional[int]

class Tontine(TontineBase):
    id: int
    creator_id: int
    created_at: datetime
    end_date: date

    class Config:
        from_attributes = True


class StatusBase(BaseModel):
    member_id: int
    tontine_id: int
    status: bool
    contributions_count: int

class StatusCreate(StatusBase):
    pass

class StatusUpdate(BaseModel):
    status: Optional[bool]
    contributions_count: Optional[int]

class Status(StatusBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token:str
    token_type:str
    role:str

class Membership(BaseModel):
    id: int
    user_id: int
    tontine_id: int
    membership_count:int
    created_at: datetime

    class Config:
        from_attributes = True

class MembershipCreate(BaseModel):
    user_id: int
    tontine_id: int
    membership_count:int

class ContributionBase(BaseModel):
    contribution_date: date
    submitted: bool

class ContributionCreate(ContributionBase):
    tontine_id: int
    membership_id: int

class Contribution(ContributionBase):
    id: int
    tontine_id: int
    membership_id: int
    created_at: datetime

    class Config:
        from_attributes = True
