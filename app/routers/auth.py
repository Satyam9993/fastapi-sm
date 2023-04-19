from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..model import models

from ..schemas import schemas
from ..db import get_db
from .. import oauth2, utils

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
def login(user_crudential:OAuth2PasswordRequestForm=Depends() ,db: Session = Depends(get_db)):
    # {
    #     "username" : "abc",
    #     "password" : "abc"
    # }
    user = db.query(models.User).filter(models.User.email == user_crudential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Authentication")

    if not utils.verify_password(user_crudential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Authentication")

    # create a token
    access_token = oauth2.create_access_token(data={"user_id":user.id})

    return { 'access_token' : access_token, 'token_type' : 'bearer' }