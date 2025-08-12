from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    username: str
    full_name: str
