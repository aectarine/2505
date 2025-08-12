import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from router.naver.login_router import router as login_router
from router.users.controller import router as user_router

app = FastAPI()

# 정적파일`
app.mount('/static', StaticFiles(directory='static'), name='static')

# 세션 (개발용: https_only=False, 운영은 True 권장)
app.add_middleware(
    SessionMiddleware,
    secret_key='super-secret-key',  # 환경변수로 교체 권장
    https_only=False,
    same_site='lax',
    max_age=60 * 60 * 24 * 7,  # 7일
)

api_app = APIRouter(prefix='/api')
page_app = APIRouter()

api_app.include_router(user_router, prefix='/users')
app.include_router(api_app)

page_app.include_router(login_router)
app.include_router(page_app)

if __name__ == '__main__':
    uvicorn.run(host='0.0.0.0', port=8000, reload=True)
