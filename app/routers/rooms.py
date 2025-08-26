from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, models
from ..deps import get_db, require_admin

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("/", response_model=list[schemas.RoomOut])
def list_rooms(db: Session = Depends(get_db)):
    rooms = db.query(models.Room).all()
    return rooms


@router.post("/", response_model=schemas.RoomOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_admin)])
def create_room(payload: schemas.RoomCreate, db: Session = Depends(get_db)):
    # можно использовать crud.create_room, если уже есть; здесь показываю прямой вариант
    room = models.Room(name=payload.name, capacity=payload.capacity)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@router.get("/{room_id}", response_model=schemas.RoomOut)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(models.Room).get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room
