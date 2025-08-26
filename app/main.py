from fastapi import FastAPI
from .routers import users, rooms, bookings, auth

app = FastAPI(title="Room Booking API")

app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(auth.router)

