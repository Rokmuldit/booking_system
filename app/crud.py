from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status

from . import models, schemas


# ---------- USER CRUD ----------

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user  # ORM


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# ---------- ROOM CRUD  ----------

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name, capacity=room.capacity)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room  # ORM

def list_rooms(db: Session):
    return db.query(models.Room).all()


# ---------- BOOKING CRUD ----------

def create_booking(db: Session, owner_id: int, booking: schemas.BookingCreate):
    """Создание нового бронирования (с проверкой пересечений)."""

    # Проверка пересечения
    overlapping = db.query(models.Booking).filter(
        models.Booking.room_id == booking.room_id,
        and_(
            models.Booking.start_time < booking.end_time,
            models.Booking.end_time > booking.start_time
        )
    ).first()

    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Выбранное время пересекается с другим бронированием"
        )

    db_booking = models.Booking(
        owner_id=owner_id,
        room_id=booking.room_id,
        start_time=booking.start_time,
        end_time=booking.end_time,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking  # ORM


def join_booking(db: Session, user_id: int, booking_id: int):
    """Пользователь присоединяется к бронированию как гость."""

    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")

    room = booking.room
    if len(booking.guests) + 1 > room.capacity:  # +1 владелец
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Комната достигла максимальной вместимости"
        )

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if user in booking.guests:
        raise HTTPException(status_code=400, detail="Пользователь уже в бронировании")

    booking.guests.append(user)
    db.commit()
    db.refresh(booking)
    return booking  # ORM


def list_bookings(db: Session):
    return db.query(models.Booking).all()


def get_user_bookings(db: Session, user_id: int):
    """Список бронирований пользователя (как владелец или как гость)."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return {
        "as_owner": user.bookings,
        "as_guest": user.guest_bookings
    }
