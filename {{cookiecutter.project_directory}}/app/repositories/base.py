from typing import TypeVar, Generic, Type, Optional, Any, Iterable
from tortoise.models import Model


ModelType = TypeVar("ModelType", bound=Model)


class CRUDBase(Generic[ModelType]):
    __slots__ = ("model",)

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, **kwargs: Any) -> ModelType:
        _model = await self.model.create(**kwargs)
        return _model

    async def filter(self, **filter: Any) -> Optional[ModelType]:
        _model = await self.model.filter(**filter).first()
        return _model

    async def filter_all(self, **filter: Any) -> Optional[ModelType]:
        _models = await self.model.filter(**filter).all()
        return _models

    async def get(self, **filter: Any) -> ModelType:
        _model = await self.model.get(**filter).first()
        return _model

    async def get_all(self, **filter: Any) -> Iterable[ModelType]:
        _models = await self.model.get(**filter).all()
        return _models
