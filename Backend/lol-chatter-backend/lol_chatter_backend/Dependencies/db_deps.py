from typing import Generator
from lol_chatter_backend.DbInitialization.db import SessionLocal
from sqlalchemy.orm import Session

def get_db() -> Generator[Session , None , None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
