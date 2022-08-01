from typing import Optional

###
from app.models import User
from app.repositories import UserRepo


class UserService:
    __slots__ = ("_user_repo",)

    def __init__(self, user_repo: UserRepo) -> None:
        self._user_repo = user_repo

    async def filter_by_mail(self, email: str) -> Optional[User]:
        model = await self._user_repo.filter(email=email)
        return model
