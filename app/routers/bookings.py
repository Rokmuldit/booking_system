from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemas, crud, models
from ..deps import get_db, get_current_user, require_admin

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/", response_model=schemas.BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(payload: schemas.BookingCreate,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    booking = crud.create_booking(db=db, owner_id=current_user.id, booking=payload)
    return booking


@router.post("/{booking_id}/join", response_model=schemas.BookingOut)
def join_booking(booking_id: int,
                 db: Session = Depends(get_db),
                 current_user: models.User = Depends(get_current_user)):
    booking = crud.join_booking(db=db, user_id=current_user.id, booking_id=booking_id)
    return booking


@router.get("/", response_model=list[schemas.BookingOut])
def list_all_bookings(db: Session = Depends(get_db)):
    return crud.list_bookings(db)
