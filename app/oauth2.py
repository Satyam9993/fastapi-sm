from jose import JWTError, jwt
from datetime import datetime, timedelta
from .model import models
from .schemas import schemas
from . import db
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Sceret_key
SCERET_KEY = settings.secret_key
# algorithm
ALGORITHM = settings.algorithm
# expression_time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_time

def create_access_token(data : dict):
    to_encode = data.copy()

    # adding expire time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SCERET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# access token verifiaction
def verify_access_token(token : str, crudential_exception):
    try:
        payload = jwt.decode(token, SCERET_KEY, algorithms=ALGORITHM)
        id : str = payload.get("user_id")
        
        if id is None:
            raise crudential_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise crudential_exception
    
    return token_data


# milldleware
def get_current_user(token : str=Depends(Oauth2_scheme), db: Session = Depends(db.get_db)):
    crudential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate crudential", headers={"WWW-Authenticate":"Bearer"})

    token = verify_access_token(token, crudential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user