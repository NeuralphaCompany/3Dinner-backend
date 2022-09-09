from datetime import timedelta
from typing import Any

from fastapi import Depends, HTTPException, APIRouter, Body
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.services import crud
from app import models, schemas
from app.core import security
from app.core.config import get_app_settings
from app.api.dependencies import db

settings = get_app_settings()

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(db.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.employee.authenticate(
        db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect email or password")
    elif not crud.employee.is_active(db=db, user=user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(
        minutes=settings.access_token_expires_minutes)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
