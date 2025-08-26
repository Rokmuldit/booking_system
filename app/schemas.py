from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


# ---------- User ----------
class UserCreate(BaseModel):
    email: str = Field(..., pattern=r"^\S+@\S+\.\S+$")
    password: str = Field(..., min_length=6)


class UserOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    email: str
    is_admin: bool


# ---------- Room ----------
class RoomCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    capacity: int = Field(..., gt=0)


class RoomOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str
    capacity: int


# ---------- Booking ----------
class BookingCreate(BaseModel):
    room_id: int = Field(..., gt=0)
    start_time: datetime
    end_time: datetime

    @field_validator("end_time")
    @classmethod
    def check_time(cls, v: datetime, info):
        start_time = info.data.get("start_time")
        if start_time and v <= start_time:
            raise ValueError("end_time must be later than start_time")
        return v


class BookingOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    start_time: datetime
    end_time: datetime
    room: RoomOut
    owner: UserOut
    guests: List[UserOut] = []
