from typing import Optional

###
from app.repositories import CRUDBase
from app.models import User


class UserRepository(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=User)

    async def filter_by_mail(self, email: str) -> Optional[User]:
        model = await self.filter(email=email)
        return model
