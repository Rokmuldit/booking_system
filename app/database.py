import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
)

@event.listens_for(engine, "connect")
def set_client_encoding(dbapi_conn, _):
    cur = dbapi_conn.cursor()
    cur.execute("SET client_encoding TO 'UTF8'")
    cur.close()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

Base = declarative_base()