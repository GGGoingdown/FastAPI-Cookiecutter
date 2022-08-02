###
from app.models import User
from app.repositories import UserRepo


class UserService:
    __slots__ = ("_user_repo",)

    def __init__(self, user_repo: UserRepo) -> None:
        self._user_repo = user_repo

    async def create_user(self, *, name: str, email: str, password_hash: str) -> User:
        return await self._user_repo.create(
            name=name, email=email, password_hash=password_hash
        )

    async def get_user_by_email(self, email: str) -> User:
        return await self._user_repo.get(email=email)
