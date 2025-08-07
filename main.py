import uvicorn
from fastapi import FastAPI, APIRouter

from users.controller import router as user_router

app = FastAPI()

api_app = APIRouter(prefix='/api')

api_app.include_router(user_router, prefix='/users')
app.include_router(api_app)

if __name__ == '__main__':
    uvicorn.run(host='0.0.0.0', port=8000, debug=True)
