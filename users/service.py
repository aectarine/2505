from typing import Optional

from users.schemas import UserLogin, UserInfo

FAKE_USERS_DB = {
    'john': {'username': 'john', 'password': 'secret', 'full_name': 'John Doe'}
}


class UserService:
    user = None

    def authenticate_user(self, login_data: UserLogin) -> Optional[UserInfo]:
        self.user = FAKE_USERS_DB.get(login_data.username)
        if self.user and self.user['password'] == login_data.password:
            return UserInfo(username=self.user['username'], full_name=self.user['full_name'])
        return None

    def get_user_info(self, username: str) -> Optional[UserInfo]:
        self.user = FAKE_USERS_DB.get(username)
        if self.user:
            return UserInfo(username=self.user['username'], full_name=self.user['full_name'])
        return None
