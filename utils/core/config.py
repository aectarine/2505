import os
from datetime import timedelta

SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def access_token_expiry():
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
