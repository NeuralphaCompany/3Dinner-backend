from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from app import schemas
from app.services import crud

from app.db import session, base

def init_db(db:Session) -> None:
    base.Base.metadata.create_all(bind=session.engine)
