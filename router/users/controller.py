from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from fastapi_utils.cbv import cbv

from utils.auth.jwt import create_access_token
from utils.auth.schemas import Token, TokenData
from utils.auth.service import get_current_user
from router.users.schemas import UserLogin, UserInfo
from router.users.service import UserService

router = APIRouter()


@cbv(router)
class UserController:
    def __init__(self, user_service: UserService = Depends()):
        self.user_service = user_service

    # 로그인 -> JWT 토큰 발급
    @router.post('/login', response_model=Token)
    async def login(self, user: UserLogin):
        auth_user = self.user_service.authenticate_user(user)
        if not auth_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Credentials'
            )
        token = create_access_token(data={'sub': auth_user.username})
        return Token(access_token=token, token_type='bearer')

    # JWT로 보호된 API -> 현재 로그인 사용자 정보
    @router.get('/me', response_model=UserInfo)
    async def get_me(self, token_data: TokenData = Depends(get_current_user)):
        user = self.user_service.get_user_info(token_data.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User Not Found'
            )
        return user
