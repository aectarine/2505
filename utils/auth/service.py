from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import status

from utils.auth.jwt import decode_access_token
from utils.auth.schemas import TokenData

# Bearer <토큰> 추출 -> token에 값 자동 주입
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        return decode_access_token(token)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or Expired Token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
