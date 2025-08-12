from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_utils.cbv import cbv
from starlette.responses import JSONResponse, RedirectResponse

router = APIRouter()

templates = Jinja2Templates(directory='templates', auto_reload=True)

NAVER_CALLBACK = 'http://localhost:8000/callback'

# OAuth 설정
oauth = OAuth()
oauth.register(
    name='naver',
    client_id='X7G_jrxUCPtObkR0ZGoH',
    client_secret='VNZIS5yucm',
    access_token_url='https://nid.naver.com/oauth2.0/token',
    access_token_params=None,
    authorize_url='https://nid.naver.com/oauth2.0/authorize',
    authorize_params=None,
    api_base_url='https://openapi.naver.com/v1/nid/',
    client_kwargs={
        # 네이버는 scope가 선택항목인데, 이메일/이름을 원하면 동의항목을 콘솔에서 켜고 scope 지정
        'scope': 'name email nickname profile_image gender birthday age birthyear mobile',
        'token_endpoint_auth_method': 'client_secret_post',  # 안전하게 토큰 교환
    }
)


@cbv(router)
class LoginRouter:
    def __init__(self):
        pass

    @router.get('/', response_class=HTMLResponse)
    def index(self, req: Request):
        return templates.TemplateResponse('index.html', {
            'request': req,
            'user': req.session.get('user')
        })

    # 네이버 로그인 요청 -> 네이버 페이지 리다이렉트
    @router.get('/login')
    async def login(self, req: Request):
        # 콜백 URL은 콘솔 등록값과 동일해야 함
        return await oauth.naver.authorize_redirect(req, NAVER_CALLBACK)

    # 네이버 콜백 -> 토큰 획득 + 사용자 정보 조회
    @router.get('/callback')
    async def callback(self, req: Request):
        token = await oauth.naver.authorize_access_token(req)
        # 프로필 조회
        resp = await oauth.naver.get('me', token=token)
        data = resp.json()  # {"resultcode":"00","message":"success","response":{...}}
        if data.get('resultcode') != '00':
            return JSONResponse({
                'error': 'NAVER_LOGIN_FAILED',
                'detail': data,
            }, status_code=status.HTTP_400_BAD_REQUEST)
        profile = data.get('response', {})
        print(profile)
        print(profile.get('address'))
        req.session['user'] = {
            'id': profile.get('id'),
            'name': profile.get('name'),
            'nickname': profile.get('nickname'),
            'email': profile.get('email'),
            'mobile': profile.get('mobile'),
            'address': profile.get('address'),
            'gender': profile.get('gender'),
            'birthday': profile.get('birthday'),
            'age': profile.get('age'),
            'birthyear': profile.get('birthyear'),
            'profile_image': profile.get('profile_image'),
        }
        # 로그인 후 메인으로
        return RedirectResponse('/')

    @router.get('/logout')
    async def logout(self, req: Request):
        req.session.clear()
        return RedirectResponse('/')
