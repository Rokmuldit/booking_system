from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from .. import schemas, crud, models, auth
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(payload.password)
    user = crud.create_user(db, payload, hashed_password=hashed_password)
    return user


@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


class UserBookingsOut(BaseModel):
    as_owner: List[schemas.BookingOut]
    as_guest: List[schemas.BookingOut]

@router.get("/me/bookings", response_model=UserBookingsOut)
def my_bookings(db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    data = crud.get_user_bookings(db, current_user.id)
    return data