from datetime import timedelta, datetime
from typing import Optional

from jose import jwt, JWTError

from auth.schemas import TokenData
from core.config import access_token_expiry, SECRET_KEY, ALGORITHM


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or access_token_expiry())
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise JWTError('Invalid Token')
        return TokenData(username=username)
    except JWTError:
        raise
